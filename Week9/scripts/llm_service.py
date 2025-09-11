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

    _llm_providers = {
        "openai": lambda: ChatOpenAI(
            model=OPENAI_CHAT_MODEL, temperature=OPENAI_TEMPERATURE
        ),
        "ollama": lambda: ChatOllama(
            model=OLLAMA_MODEL, temperature=OLLAMA_TEMPERATURE
        ),
    }

    @staticmethod
    def get_llm(provider: str = DEFAULT_LLM_PROVIDER):
        """
        Return the correct LLM client based on provider.

        Args:
            provider (str): "openai" or "ollama"

        Returns:
            ChatOpenAI | ChatOllama
        """
        if provider not in LLMService._llm_providers:
            logger.warning(
                f"Unknown provider '{provider}', defaulting to {DEFAULT_LLM_PROVIDER}"
            )
            provider = DEFAULT_LLM_PROVIDER

        logger.info(f"Using '{provider}' as LLM provider.")
        return LLMService._llm_providers[provider]()
