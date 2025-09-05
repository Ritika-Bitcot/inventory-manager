# Week8/scripts/db_utils.py
import logging
import os

from dotenv import load_dotenv
from langchain_community.vectorstores.pgvector import PGVector
from langchain_openai import OpenAIEmbeddings

from .constant import MODEL_NAME_EMBEDDING, PGVECTOR_COLLECTION_NAME

load_dotenv()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def get_db_url() -> str:
    """
    Return the database URL.
    """
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL not found in environment variables")
    return db_url


def load_vector_store(collection_name: str = PGVECTOR_COLLECTION_NAME) -> PGVector:
    """
    Load the vector store from a Postgres database.
    """
    db_url = get_db_url()
    logger.info(f"Loading vector store from collection '{collection_name}'...")

    embeddings = OpenAIEmbeddings(model=MODEL_NAME_EMBEDDING)
    vector_store = PGVector(
        collection_name=collection_name,
        connection_string=db_url,
        embedding_function=embeddings,
    )
    return vector_store
