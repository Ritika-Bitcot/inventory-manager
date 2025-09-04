import logging
import sys

from data_loader import ProductDataLoader
from db_utils import connect_db, init_flask_app
from dotenv import load_dotenv
from embedding import EmbeddingPipeline
from rag_chain import RAGChainBuilder

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)


def run_rag_pipeline(question: str) -> str:
    """End-to-end RAG pipeline execution."""
    try:
        # Step 1: DB connection + Flask app
        conn, _ = connect_db()
        app, db = init_flask_app()

        # Step 2: Load product data
        loader = ProductDataLoader(app, db)
        texts = loader.load()

        # Step 3: Embedding + vector store
        embedder = EmbeddingPipeline(conn)
        vectorstore = embedder.store_embeddings(texts)

        # Step 4: Create retriever + RAG chain
        retriever = vectorstore.as_retriever()
        rag_chain = RAGChainBuilder(retriever).build_chain()

        # Step 5: Run query
        return rag_chain.invoke(question)
    except Exception as e:
        logging.error("Pipeline execution failed: %s", str(e))
        raise


if __name__ == "__main__":
    sample_question = "What products are available in the database?"
    answer = run_rag_pipeline(sample_question)
    logging.info("Answer: %s", answer)
