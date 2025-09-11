# Week8/scripts/rag_chain.py
import logging
from typing import Union

from dotenv import load_dotenv
from langchain.schema import StrOutputParser
from langchain_community.chat_models import ChatOllama
from langchain_community.vectorstores.pgvector import PGVector
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnablePassthrough
from langchain_openai import ChatOpenAI
from prompts.system_prompt import RAG_PROMPT_TEMPLATE

from .constant import DEFAULT_LLM_PROVIDER, RETRIEVER_TOP_K
from .llm_service import LLMService

load_dotenv()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def build_rag_chain(
    vector_store: PGVector, provider: str = DEFAULT_LLM_PROVIDER
) -> Runnable:
    """Build a Retrieval-Augmented Generation (RAG) chain."""
    try:
        retriever = vector_store.as_retriever(search_kwargs={"k": RETRIEVER_TOP_K})
        logger.info(f"Retriever will fetch top {RETRIEVER_TOP_K} documents")

        prompt = ChatPromptTemplate.from_template(RAG_PROMPT_TEMPLATE)

        llm: Union[ChatOpenAI, ChatOllama] = LLMService.get_llm(provider)
        logger.info(f"Building RAG chain with LLM provider: {provider}")

        chain = (
            {
                "context": retriever
                | (lambda docs: "\n\n".join([doc.page_content for doc in docs])),
                "question": RunnablePassthrough(),
            }
            | prompt
            | llm
            | StrOutputParser()
        )
        return chain

    except Exception as e:
        logger.error(f"Error building RAG chain: {e}", exc_info=True)
        raise
