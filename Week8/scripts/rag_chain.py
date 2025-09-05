# Week8/scripts/rag_chain.py
import logging

from constant import (
    OPENAI_CHAT_MODEL,
    OPENAI_TEMPERATURE,
    RAG_PROMPT_TEMPLATE,
)
from dotenv import load_dotenv
from langchain.schema import StrOutputParser
from langchain_community.vectorstores.pgvector import PGVector
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

load_dotenv()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def build_rag_chain(vector_store: PGVector) -> ChatOpenAI:
    """Build a Retrieval-Augmented Generation (RAG) chain."""
    retriever = vector_store.as_retriever()
    prompt = ChatPromptTemplate.from_template(RAG_PROMPT_TEMPLATE)
    llm = ChatOpenAI(model=OPENAI_CHAT_MODEL, temperature=OPENAI_TEMPERATURE)

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain
