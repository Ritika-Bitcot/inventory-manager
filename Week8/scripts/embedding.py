import logging
import os
from typing import List

from constant import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    MODEL_NAME_EMBEDDING,
    PGVECTOR_COLLECTION_NAME,
)
from langchain_community.vectorstores.pgvector import PGVector
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from psycopg2.extensions import connection


class EmbeddingPipeline:
    """Handles text chunking, embedding, and storage in pgvector."""

    def __init__(self, conn: connection) -> None:
        self.conn = conn
        self.embedding_model = OpenAIEmbeddings(model=MODEL_NAME_EMBEDDING)

    def store_embeddings(self, texts: List[str]) -> PGVector:
        try:
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
            )
            chunks = splitter.split_text("\n".join(texts))

            connection_string = (
                f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
                f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
            )

            vectorstore = PGVector.from_texts(
                embedding=self.embedding_model,
                texts=chunks,
                collection_name=PGVECTOR_COLLECTION_NAME,
                connection_string=connection_string,
            )

            logging.info("✅ Successfully stored %d chunks in pgvector", len(chunks))
            return vectorstore
        except Exception as e:
            logging.error("Error generating or storing embeddings: %s", str(e))
            raise
