import logging

from flask import Blueprint, jsonify, request
from scripts.data_loader import load_products
from scripts.db_utils import get_db_url, load_vector_store
from scripts.embedding import embed_and_store
from scripts.rag_chain import build_rag_chain

from ..decorators import jwt_required

logger = logging.getLogger(__name__)
chat_bp = Blueprint("chat", __name__, url_prefix="/chat")

try:
    logger.info("Initializing RAG chain for chat endpoint...")
    vector_store = load_vector_store()

    if not vector_store.similarity_search("test", k=15):
        raise ValueError("No embeddings found, running ingestion")

except Exception as e:
    logger.warning(f"{e}")
    db_url = get_db_url()
    products = load_products(db_url)
    vector_store = embed_and_store(products)

rag_chain = build_rag_chain(vector_store)


@jwt_required
@chat_bp.route("/inventory", methods=["POST"])
def chat_inventory():
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

        answer = rag_chain.invoke(question)
        return jsonify({"answer": answer})

    except Exception as e:
        logger.exception("Error in /chat/inventory")
        return jsonify({"error": str(e)}), 500
