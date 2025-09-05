import logging
import os
import sys
import warnings

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from data_loader import load_products
from db_utils import get_db_url, load_vector_store
from dotenv import load_dotenv
from embedding import embed_and_store
from rag_chain import build_rag_chain

load_dotenv()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Suppress noisy warnings from langchain
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=PendingDeprecationWarning)


def main() -> None:
    """
    Main script to:
    1. Load existing embeddings from vector DB.
    2. Run embedding ingestion for new products (if any).
    3. Build RAG chain using updated embeddings.
    4. Example query to RAG chain.
    """
    logger.info("Loading vector store...")
    vector_store = load_vector_store()

    db_url = get_db_url()
    products = load_products(db_url)

    # Get product IDs that already exist in vector store
    existing_docs = vector_store.similarity_search("", k=1000)
    existing_ids = {doc.metadata.get("product_id") for doc in existing_docs}

    # Find new products not yet embedded
    new_products = [p for p in products if p["product_id"] not in existing_ids]

    if new_products:
        logger.info(f"Found {len(new_products)} new products. Embedding them now...")
        embed_and_store(new_products)
        vector_store = load_vector_store()

    else:
        logger.info("No new products to embed.")

    logger.info("Building RAG chain...")
    rag_chain = build_rag_chain(vector_store)

    question = "What products available in food category?"
    logger.info(f"Asking RAG chain: {question}")
    answer = rag_chain.invoke(question)

    print("\n=== RAG Answer ===")
    print(answer)


if __name__ == "__main__":
    main()
