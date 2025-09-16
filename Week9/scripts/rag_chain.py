import logging

from dotenv import load_dotenv
from langchain.schema import StrOutputParser
from langchain_community.vectorstores.pgvector import PGVector
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from prompts.system_prompt import RAG_PROMPT_TEMPLATE

from .constant import DEFAULT_LLM_PROVIDER, RETRIEVER_TOP_K
from .llm_service import LLMService

load_dotenv()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def build_rag_chain(
    vector_store: PGVector, user_id: str, provider: str = DEFAULT_LLM_PROVIDER
):
    """Build RAG chain strictly per user."""
    search_kwargs = {"k": RETRIEVER_TOP_K, "filter": {"user_id": str(user_id)}}
    retriever = vector_store.as_retriever(search_kwargs=search_kwargs)

    prompt = ChatPromptTemplate.from_template(RAG_PROMPT_TEMPLATE)
    llm = LLMService.get_llm(provider)

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
