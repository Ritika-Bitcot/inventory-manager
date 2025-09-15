# Week9/api/routes/chat.py
import logging

from flask import Blueprint, g, jsonify, request
from langchain_community.vectorstores.pgvector import PGVector
from scripts.constant import DEFAULT_LLM_PROVIDER
from scripts.data_loader import load_products
from scripts.db_utils import SQLAlchemyCache, get_db_url, load_vector_store
from scripts.embedding import embed_and_store
from scripts.rag_chain import build_rag_chain

from ..db import db
from ..decorators import jwt_required

logger = logging.getLogger(__name__)
chat_bp = Blueprint("chat", __name__, url_prefix="/chat")


def refresh_vector_store(user_id: str) -> PGVector:
    """Refresh vector store for a user."""
    products = load_products(get_db_url())
    vector_store = load_vector_store()

    existing_docs = vector_store.similarity_search("", k=1000)
    existing_ids = {
        doc.metadata.get("product_id")
        for doc in existing_docs
        if doc.metadata.get("user_id") == user_id
    }

    new_products = [p for p in products if p["product_id"] not in existing_ids]

    if new_products:
        vector_store = embed_and_store(new_products, user_id=user_id) or vector_store

    return vector_store


@chat_bp.route("/inventory", methods=["POST"])
@jwt_required
def chat_inventory():
    data = request.get_json()
    if not data or "question" not in data:
        return jsonify({"error": "Missing 'question'"}), 400

    question = data["question"]
    provider = data.get("provider", DEFAULT_LLM_PROVIDER)
    user_id = g.current_user.get("id")

    session = db.session
    cache = SQLAlchemyCache(session)
    cache.clear_expired()

    cached = cache.get_cached_response(prompt=question, user_id=user_id, model=provider)
    if cached:
        return jsonify({"answer": cached.response, "cached": True})

    vector_store = refresh_vector_store(user_id=user_id)
    rag_chain = build_rag_chain(
        vector_store=vector_store, user_id=user_id, provider=provider
    )
    answer = rag_chain.invoke(question)

    cache.save_response(
        prompt=question, response=answer, user_id=user_id, model=provider
    )
    return jsonify({"answer": answer, "cached": False, "provider": provider})
