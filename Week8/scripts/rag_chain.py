from constant import MODEL_NAME, RAG_PROMPT_TEMPLATE
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI


class RAGChainBuilder:
    """Builds the RAG chain using LCEL."""

    def __init__(self, retriever) -> None:
        self.retriever = retriever
        self.prompt = ChatPromptTemplate.from_template(RAG_PROMPT_TEMPLATE)
        self.model = ChatOpenAI(model=MODEL_NAME)

    def build_chain(self):
        """Build LCEL chain: {context, question} -> prompt -> model -> parser"""
        return (
            {
                "context": self.retriever,
                "question": RunnablePassthrough(),
            }
            | self.prompt
            | self.model
            | StrOutputParser()
        )
