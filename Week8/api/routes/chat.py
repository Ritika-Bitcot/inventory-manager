import logging

from flask import Blueprint, jsonify, request
from langchain_community.vectorstores.pgvector import PGVector
from scripts.data_loader import load_products
from scripts.db_utils import get_db_url, load_vector_store
from scripts.embedding import embed_and_store
from scripts.rag_chain import build_rag_chain

from ..decorators import jwt_required

logger = logging.getLogger(__name__)
chat_bp = Blueprint("chat", __name__, url_prefix="/chat")


def refresh_vector_store() -> PGVector:
    """
    Sync vector store with DB before answering.
    Ensures newly added products get embedded.
    """
    db_url = get_db_url()
    products = load_products(db_url)

    vector_store = load_vector_store()

    existing_docs = vector_store.similarity_search("", k=1000)
    existing_ids = {doc.metadata.get("product_id") for doc in existing_docs}

    new_products = [p for p in products if p["product_id"] not in existing_ids]

    if new_products:
        logger.info(f"Found {len(new_products)} new products → embedding them...")
        vector_store = embed_and_store(new_products) or vector_store
    else:
        logger.info("No new products to embed.")

    return vector_store


@jwt_required
@chat_bp.route("/inventory", methods=["POST"])
def chat_inventory() -> jsonify:
    """
    POST /chat/inventory
    Body: { "question": "What products are available in food category?" }
    """
    try:
        data = request.get_json()
        if not data or "question" not in data:
            return jsonify({"error": "Missing 'question'"}), 400

        question = data["question"]
        logger.info(f"User asked: {question}")

        vector_store = refresh_vector_store()
        rag_chain = build_rag_chain(vector_store)

        answer = rag_chain.invoke(question)
        return jsonify({"answer": answer})

    except Exception as e:
        logger.exception("Error in /chat/inventory")
        return jsonify({"error": str(e)}), 500
