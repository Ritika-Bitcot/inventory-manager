# Week8/scripts/embedding.py
import logging
from typing import Dict, List

from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.pgvector import PGVector
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from scripts.db_utils import get_db_url

from .constant import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    MODEL_NAME_EMBEDDING,
    PGVECTOR_COLLECTION_NAME,
)

load_dotenv()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def embed_and_store(products: List[Dict]) -> None:
    """
    Embed new products and add them to the existing PGVector collection.
    """
    db_url = get_db_url()
    logger.info("Initializing OpenAI embeddings...")
    embeddings = OpenAIEmbeddings(model=MODEL_NAME_EMBEDDING)

    logger.info("Splitting product data into chunks...")
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
                    },
                )
            )

    logger.info(f"Generated {len(documents)} chunks for embedding.")

    vector_store = PGVector(
        connection_string=db_url,
        collection_name=PGVECTOR_COLLECTION_NAME,
        embedding_function=embeddings,
    )

    vector_store.add_documents(documents)
    logger.info("✅ Embeddings successfully stored in PGVector.")
