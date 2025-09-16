import logging
import os
from datetime import datetime, timedelta, timezone
from typing import List, Optional

from api.models import LLMCache
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.pgvector import PGVector

from .constant import DEFAULT_CACHE_MODEL, PGVECTOR_COLLECTION_NAME
from .embedding_service import EmbeddingService

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
        embeddings = EmbeddingService.get_huggingface_embeddings()
        vector_store = PGVector(
            collection_name=collection_name,
            connection_string=db_url,
            embedding_function=embeddings,
        )
        return vector_store
    except Exception as e:
        logger.error(f"Error loading vector store: {e}", exc_info=True)
        raise


def store_document_vectors(
    user_id: Optional[str],
    document_id: int,
    content: str,
    embedding_instance,
    collection_name: str = PGVECTOR_COLLECTION_NAME,
    chunk_size: int = 500,
    chunk_overlap: int = 50,
) -> None:
    """
    Chunk a document, generate embeddings, and store in pgvector with metadata.

    Args:
        user_id (str | None): The ID of the user uploading the document.
        If None, treated as global.
        document_id (int): The database ID of the document.
        content (str): The raw text content of the document.
        embedding_instance: An already-initialized embedding
          object (e.g., HuggingFaceEmbeddings).
        collection_name (str): Name of pgvector collection.
        chunk_size (int): Max size of text chunks.
        chunk_overlap (int): Overlap between chunks.
    """
    try:
        db_url = get_db_url()

        # Split document into chunks
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )
        chunks: List[str] = splitter.split_text(content)

        if not chunks:
            logger.warning("No content chunks generated from document.")
            return

        # embedding_instance should be an actual embeddings object (not the class)
        embeddings = embedding_instance

        # Create vector store
        vector_store = PGVector(
            collection_name=collection_name,
            connection_string=db_url,
            embedding_function=embeddings,
        )

        # Normalize user_id metadata: use GLOBAL_USER_ID
        # string for global docs to match retriever
        normalized_user_id = str(user_id)

        # Add chunks with metadata
        metadatas = [
            {"user_id": normalized_user_id, "document_id": str(document_id), "chunk": i}
            for i in range(len(chunks))
        ]
        vector_store.add_texts(texts=chunks, metadatas=metadatas)

        logger.info(
            f"""Stored {len(chunks)} chunks for document_id={document_id},
            user_id={normalized_user_id}"""
        )
    except Exception as e:
        logger.error(f"Error storing document vectors: {e}", exc_info=True)
        raise


class SQLAlchemyCache:
    def __init__(self, db_session, ttl_seconds: int = 3600):
        """Initialize cache with a SQLAlchemy session and TTL."""
        self.db = db_session
        self.ttl_seconds = ttl_seconds

    def clear_expired(self):
        """Remove expired cache entries."""
        try:
            now = datetime.now(timezone.utc)
            self.db.query(LLMCache).filter(LLMCache.expires_at <= now).delete()
            self.db.commit()
        except Exception as e:
            logger.error(f"Error clearing expired cache: {e}", exc_info=True)
            self.db.rollback()

    def get_cached_response(
        self, prompt: str, user_id: str, model: str = DEFAULT_CACHE_MODEL
    ):
        """Retrieve user-specific cache (no global fallback)."""
        try:
            now = datetime.now(timezone.utc)
            return (
                self.db.query(LLMCache)
                .filter(
                    LLMCache.prompt == prompt,
                    LLMCache.model == model,
                    LLMCache.expires_at > now,
                    LLMCache.user_id == user_id,
                )
                .first()
            )
        except Exception as e:
            logger.error(f"Error fetching cache: {e}", exc_info=True)
            return None

    def save_response(
        self, prompt: str, response: str, user_id: str, model: str = DEFAULT_CACHE_MODEL
    ):
        """Save user-specific response."""
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
            logger.info(
                f"Cached response for user_id={user_id}, prompt={prompt[:30]}..."
            )
            return cache_entry
        except Exception as e:
            logger.error(f"Error saving cache: {e}", exc_info=True)
            self.db.rollback()
            return None
