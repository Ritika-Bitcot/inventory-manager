# Week8/scripts/embedding.py
import logging
from typing import Dict, List

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


def embed_and_store(products: List[Dict], user_id: str) -> PGVector:
    """
    Embed new products and store in PGVector strictly for a user.
    """
    if not products:
        logger.warning("No products provided for embedding.")
        return

    db_url = get_db_url()
    embeddings = EmbeddingService.get_huggingface_embeddings()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    )

    documents: list[Document] = []
    for product in products:
        content = f"{product['product_name']}\n{product['description']}"
        for chunk in text_splitter.split_text(content):
            documents.append(
                Document(
                    page_content=chunk,
                    metadata={
                        "product_id": product["product_id"],
                        "name": product["product_name"],
                        "user_id": user_id,
                    },
                )
            )

    vector_store = PGVector(
        connection_string=db_url,
        collection_name=PGVECTOR_COLLECTION_NAME,
        embedding_function=embeddings,
    )
    vector_store.add_documents(documents)
    logger.info(f"✅ Stored {len(documents)} chunks for user_id={user_id}")
    return vector_store
