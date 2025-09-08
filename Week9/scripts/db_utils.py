# Week8/scripts/db_utils.py
import logging
import os
from typing import Optional

from api.models import LLMCache
from dotenv import load_dotenv
from langchain_community.vectorstores.pgvector import PGVector
from langchain_openai import OpenAIEmbeddings
from sqlalchemy.orm import Session

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
        logger.error("DATABASE_URL not found in environment variables.")
        raise ValueError("DATABASE_URL not found in environment variables")

    return db_url


def load_vector_store(collection_name: str = PGVECTOR_COLLECTION_NAME) -> PGVector:
    """
    Load the vector store from a Postgres database.
    """
    try:
        db_url = get_db_url()
        logger.info(f"Loading vector store from collection '{collection_name}'...")

        embeddings = OpenAIEmbeddings(model=MODEL_NAME_EMBEDDING)
        vector_store = PGVector(
            collection_name=collection_name,
            connection_string=db_url,
            embedding_function=embeddings,
        )
        return vector_store

    except Exception as e:
        logger.error(f"Error loading vector store: {e}", exc_info=True)
        raise


class SQLAlchemyCache:
    """Cache handler for storing and retrieving LLM responses."""

    def __init__(self, db_session: Session) -> None:
        self.db = db_session

    def get_cached_response(
        self, prompt: str, user_id: Optional[str] = None, model: str = "openai"
    ) -> Optional[LLMCache]:
        """
        Retrieve cached LLM response if available.

        Args:
            prompt (str): The LLM prompt/question.
            user_id (str, optional): User ID for multi-tenant cache. Defaults to None.
            model (str): Model name (e.g., OpenAI or Ollama). Defaults to "openai".

        Returns:
            Optional[LLMCache]: Cached response object if exists, else None.
        """
        try:
            query = self.db.query(LLMCache).filter(
                LLMCache.prompt == prompt, LLMCache.model == model
            )
            if user_id:
                query = query.filter(LLMCache.user_id == user_id)
            else:
                query = query.filter(LLMCache.user_id.is_(None))
            return query.first()
        except Exception as e:
            logger.error(f"Error fetching cache: {e}", exc_info=True)
            return None

    def save_response(
        self,
        prompt: str,
        response: str,
        user_id: Optional[str] = None,
        model: str = "openai",
    ) -> Optional[LLMCache]:
        """
        Save a new LLM response to the cache.

        Args:
            prompt (str): The prompt/question.
            response (str): The LLM response.
            user_id (str, optional): User ID for multi-tenant cache. Defaults to None.
            model (str): Model name (e.g., OpenAI or Ollama). Defaults to "openai".

        Returns:
            Optional[LLMCache]: Saved cache object, or None on failure.
        """
        try:
            cache_entry = LLMCache(
                prompt=prompt, response=response, user_id=user_id, model=model
            )
            self.db.add(cache_entry)
            self.db.commit()
            self.db.refresh(cache_entry)
            logger.info(f"Cached response for prompt: {prompt[:30]}...")
            return cache_entry
        except Exception as e:
            logger.error(f"Error saving cache: {e}", exc_info=True)
            self.db.rollback()
            return None
