# Week9/api/routes/chat.py
import logging

from flask import Blueprint, g, jsonify, request
from langchain_postgres import PGVector
from scripts.data_loader import load_products
from scripts.db_utils import SQLAlchemyCache, get_db_url, load_vector_store
from scripts.embedding import embed_and_store
from scripts.rag_chain import build_rag_chain
from sqlalchemy.orm import Session

from ..db import db
from ..decorators import jwt_required

logger = logging.getLogger(__name__)
chat_bp = Blueprint("chat", __name__, url_prefix="/chat")


def refresh_vector_store() -> "PGVector":
    """
    Refresh the vector store to include newly added products.

    Returns:
        PGVector: Updated vector store.
    """
    try:
        db_url = get_db_url()
        products = load_products(db_url)
        vector_store = load_vector_store()

        existing_docs = vector_store.similarity_search("", k=1000)
        existing_ids = {doc.metadata.get("product_id") for doc in existing_docs}
        new_products = [p for p in products if p["product_id"] not in existing_ids]

        if new_products:
            logger.info(f"Embedding {len(new_products)} new products...")
            vector_store = embed_and_store(new_products) or vector_store
        else:
            logger.info("No new products to embed.")
        return vector_store
    except Exception as e:
        logger.error(f"Error refreshing vector store: {e}", exc_info=True)
        raise


@chat_bp.route("/inventory", methods=["POST"])
@jwt_required
def chat_inventory() -> "jsonify":
    """
    POST /chat/inventory
    Handles multi-tenant LLM caching and RAG-based answers.

    Request JSON:
        { "question": "<user_question>" }

    Returns:
        JSON response with answer and caching info.
    """
    try:
        data = request.get_json()
        if not data or "question" not in data:
            return jsonify({"error": "Missing 'question'"}), 400

        question: str = data["question"]
        current_user = g.current_user
        user_id: str = current_user.get("id") if current_user else None
        model: str = "openai"

        session: Session = db.session
        cache = SQLAlchemyCache(session)

        cached = cache.get_cached_response(
            prompt=question, user_id=user_id, model=model
        )
        if cached:
            return jsonify({"answer": cached.response, "cached": True})

        cached_global = cache.get_cached_response(
            prompt=question, user_id=None, model=model
        )
        if cached_global:
            return jsonify(
                {"answer": cached_global.response, "cached": True, "global": True}
            )

        vector_store = refresh_vector_store()
        rag_chain = build_rag_chain(vector_store)
        answer: str = rag_chain.invoke(question)

        cache.save_response(
            prompt=question, response=answer, user_id=user_id, model=model
        )

        return jsonify({"answer": answer, "cached": False})

    except Exception as e:
        logger.exception(f"Unexpected error in /chat/inventory: {e}")
        return jsonify({"error": "Internal server error"}), 500
