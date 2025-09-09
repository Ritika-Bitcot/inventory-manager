import logging
import os
from datetime import datetime, timedelta, timezone
from typing import Optional

from api.models import LLMCache
from dotenv import load_dotenv
from langchain_community.vectorstores.pgvector import PGVector
from langchain_openai import OpenAIEmbeddings
from sqlalchemy.orm import Session

from .constant import MODEL_NAME_EMBEDDING, PGVECTOR_COLLECTION_NAME

# Load environment variables
load_dotenv()

# Logger configuration
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def get_db_url() -> str:
    """
    Retrieve the database connection URL from environment variables.

    Returns:
        str: Database connection string.

    Raises:
        ValueError: If DATABASE_URL is not set.
    """
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        logger.error("DATABASE_URL not found in environment variables.")
        raise ValueError("DATABASE_URL not found in environment variables")
    return db_url


def load_vector_store(collection_name: str = PGVECTOR_COLLECTION_NAME) -> PGVector:
    """
    Load the PGVector store from PostgreSQL.

    Args:
        collection_name (str): The name of the collection/table in pgvector.

    Returns:
        PGVector: Configured PGVector store instance.

    Raises:
        Exception: If initialization fails.
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

    def __init__(self, db_session: Session, ttl_seconds: int = 3600) -> None:
        """
        Initialize SQLAlchemyCache.

        Args:
            db_session (Session): SQLAlchemy session.
            ttl_seconds (int): Time-to-live for cache entries (default 1 hour).
        """
        self.db = db_session
        self.ttl_seconds = ttl_seconds

    def get_cached_response(
        self, prompt: str, user_id: Optional[str] = None, model: str = "openai"
    ) -> Optional[LLMCache]:
        """
        Retrieve cached LLM response if available and not expired.

        Args:
            prompt (str): The LLM prompt/question.
            user_id (str, optional): User ID for multi-tenant cache.
            model (str): Model name.

        Returns:
            Optional[LLMCache]: Cached response object if exists, else None.
        """
        try:
            now = datetime.now(timezone.utc)

            query = self.db.query(LLMCache).filter(
                LLMCache.prompt == prompt,
                LLMCache.model == model,
                LLMCache.expires_at > now,
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
            user_id (str, optional): User ID for multi-tenant cache.
            model (str): Model name.

        Returns:
            Optional[LLMCache]: Saved cache object, or None on failure.
        """
        try:
            expires_at = datetime.now(timezone.utc) + timedelta(
                seconds=self.ttl_seconds
            )

            cache_entry = LLMCache(
                prompt=prompt,
                response=response,
                user_id=user_id,
                model=model,
                expires_at=expires_at,
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

    def clear_expired(self) -> int:
        """
        Delete expired cache entries.

        Returns:
            int: Count of deleted rows.
        """
        try:
            now = datetime.now(timezone.utc)
            deleted = (
                self.db.query(LLMCache).filter(LLMCache.expires_at <= now).delete()
            )
            self.db.commit()
            if deleted:
                logger.info(f"Cleared {deleted} expired cache entries.")
            return deleted
        except Exception as e:
            logger.error(f"Error clearing expired cache: {e}", exc_info=True)
            self.db.rollback()
            return 0
