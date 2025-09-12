# Week8/scripts/embedding.py
import logging
from typing import Dict, List, Optional

from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.pgvector import PGVector
from langchain_core.documents import Document
from scripts.db_utils import get_db_url

from .constant import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    PGVECTOR_COLLECTION_NAME,
)
from .embedding_service import EmbeddingService

load_dotenv()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def embed_and_store(
    products: List[Dict], user_id: Optional[str] = None
) -> Optional[PGVector]:
    """
    Embed new products and add them to the existing PGVector collection.
    """
    if not products:
        logger.warning("No products provided for embedding.")
        return

    try:
        db_url = get_db_url()
        logger.info("Initializing Hugging Face embeddings...")
        embeddings = EmbeddingService.get_huggingface_embeddings()

        logger.info("Splitting product data into chunks...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
        )

        documents: list[Document] = []
        for product in products:
            try:
                content = f"{product['product_name']}\n{product['description']}"
                for chunk in text_splitter.split_text(content):
                    meta = {
                        "product_id": product.get("product_id"),
                        "name": product.get("product_name"),
                    }
                    if user_id is not None:
                        meta["user_id"] = str(user_id)

                    if "category" in product:
                        meta["category"] = product.get("category")
                    if "price" in product:
                        meta["price"] = product.get("price")
                    if "quantity" in product:
                        meta["quantity"] = product.get("quantity")

                    documents.append(
                        Document(
                            page_content=chunk,
                            metadata=meta,
                        )
                    )

            except KeyError as e:
                logger.error(f"Missing expected product key: {e}")
                continue

        logger.info(f"Generated {len(documents)} chunks for embedding.")

        vector_store = PGVector(
            connection_string=db_url,
            collection_name=PGVECTOR_COLLECTION_NAME,
            embedding_function=embeddings,
        )

        vector_store.add_documents(documents)
        logger.info("✅ Embeddings successfully stored in PGVector.")

        return vector_store

    except Exception as e:
        logger.error(f"Error in embed_and_store: {e}", exc_info=True)
        return None
