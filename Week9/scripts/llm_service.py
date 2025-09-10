import logging

from langchain_community.chat_models import ChatOllama
from langchain_openai import ChatOpenAI

from .constant import (
    DEFAULT_LLM_PROVIDER,
    OLLAMA_MODEL,
    OLLAMA_TEMPERATURE,
    OPENAI_CHAT_MODEL,
    OPENAI_TEMPERATURE,
)

logger = logging.getLogger(__name__)


class LLMService:
    """
    Factory class for creating LLM clients (OpenAI, Ollama, etc.).
    Adheres to OCP by allowing easy extension for new providers.
    """

    @staticmethod
    def get_llm(provider: str = DEFAULT_LLM_PROVIDER):
        """
        Return the correct LLM client based on provider.

        Args:
            provider (str): "openai" or "ollama"

        Returns:
            ChatOpenAI | ChatOllama
        """
        if provider == "ollama":
            logger.info("Using Ollama (Llama 3 local) as provider.")
            return ChatOllama(model=OLLAMA_MODEL, temperature=OLLAMA_TEMPERATURE)

        logger.info("Using OpenAI as provider.")
        return ChatOpenAI(model=OPENAI_CHAT_MODEL, temperature=OPENAI_TEMPERATURE)
