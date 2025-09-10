# Week8/scripts/rag_chain.py
import logging

from dotenv import load_dotenv
from langchain.schema import StrOutputParser
from langchain_community.vectorstores.pgvector import PGVector
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnablePassthrough
from langchain_openai import ChatOpenAI
from prompts.system_prompt import RAG_PROMPT_TEMPLATE

from .constant import (
    OPENAI_CHAT_MODEL,
    OPENAI_TEMPERATURE,
)

load_dotenv()
logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.INFO)


def build_rag_chain(vector_store: PGVector) -> Runnable:
    """Build a Retrieval-Augmented Generation (RAG) chain."""
    try:
        retriever = vector_store.as_retriever(search_kwargs={"k": 10})
        prompt = ChatPromptTemplate.from_template(RAG_PROMPT_TEMPLATE)
        llm = ChatOpenAI(model=OPENAI_CHAT_MODEL, temperature=OPENAI_TEMPERATURE)

        chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
        return chain

    except Exception as e:
        logger.error(f"Error building RAG chain: {e}", exc_info=True)
        raise
