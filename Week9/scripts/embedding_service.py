import logging

from langchain_community.embeddings import HuggingFaceEmbeddings

from .constant import MODEL_NAME_EMBEDDING

logger = logging.getLogger(__name__)


class EmbeddingService:
    """
    Service responsible for initializing and providing embedding models.
    Adheres to SRP: only deals with embeddings, not DB or document handling.
    """

    @staticmethod
    def get_huggingface_embeddings() -> HuggingFaceEmbeddings:
        """
        Initialize and return a HuggingFace embedding model instance.

        Returns:
            HuggingFaceEmbeddings: Configured embedding model.

        Raises:
            Exception: If model loading fails.
        """
        try:
            logger.info(f"Loading HuggingFace embeddings: {MODEL_NAME_EMBEDDING}")
            return HuggingFaceEmbeddings(model_name=MODEL_NAME_EMBEDDING)
        except Exception as e:
            logger.error(f"Error loading HuggingFace embeddings: {e}", exc_info=True)
            raise
