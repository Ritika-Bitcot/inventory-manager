import logging
import os
import sys
from typing import List, Tuple

import psycopg2
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError
from psycopg2.extensions import connection, cursor

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)


def connect_db() -> Tuple[connection, cursor]:
    """
    Establish a connection to the PostgreSQL database.

    Returns:
        Tuple[connection, cursor]: A tuple containing the database connection
        and cursor objects.

    Raises:
        psycopg2.Error: If the database connection fails.
    """
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
        )
        return conn, conn.cursor()
    except psycopg2.Error as e:
        logging.error("❌ Database connection failed: %s", e)
        sys.exit(1)


def create_table(cur: cursor, conn: connection) -> None:
    """
    Create a 'documents' table with a pgvector column for storing embeddings.

    Args:
        cur (cursor): Database cursor.
        conn (connection): Database connection.
    """
    try:
        cur.execute(
            """
        CREATE TABLE IF NOT EXISTS documents (
            id SERIAL PRIMARY KEY,
            content TEXT,
            embedding VECTOR(1536)
        );
        """
        )
        conn.commit()
        logging.info("✅ Table 'documents' is ready.")
    except psycopg2.Error as e:
        logging.error("❌ Failed to create table: %s", e)
        conn.rollback()


def generate_embedding(client: OpenAI, text: str) -> List[float]:
    """
    Generate a text embedding using the OpenAI API.

    Args:
        client (OpenAI): OpenAI client instance.
        text (str): Input text to embed.

    Returns:
        List[float]: The embedding vector.

    Raises:
        OpenAIError: If the embedding API call fails.
    """
    try:
        response = client.embeddings.create(model="text-embedding-3-small", input=text)
        embedding = response.data[0].embedding

        if len(embedding) != 1536:
            raise ValueError(
                f"Embedding length mismatch: expected 1536, got {len(embedding)}"
            )

        return embedding
    except (OpenAIError, ValueError) as e:
        logging.error("❌ Failed to generate embedding: %s", e)
        raise


def insert_document(
    cur: cursor, conn: connection, content: str, embedding: List[float]
) -> None:
    """
    Insert a document and its embedding into the 'documents' table.

    Args:
        cur (cursor): Database cursor.
        conn (connection): Database connection.
        content (str): Text content to store.
        embedding (List[float]): Embedding vector of the content.
    """
    try:
        cur.execute(
            "INSERT INTO documents (content, embedding) VALUES (%s, %s)",
            (content, embedding),
        )
        conn.commit()
        logging.info("✅ Inserted document: %s", content)
    except psycopg2.Error as e:
        logging.error("❌ Failed to insert document: %s", e)
        conn.rollback()


def main() -> None:
    """
    Main script to:
    1. Connect to PostgreSQL.
    2. Create a 'documents' table with vector support.
    3. Generate embeddings for sample sentences.
    4. Store them in the database.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    conn, cur = connect_db()

    try:
        create_table(cur, conn)

        sentences = [
            "Bananas are a healthy snack.",
            "Apples can be red, green, or yellow.",
            "Oranges are rich in Vitamin C.",
        ]

        for sentence in sentences:
            try:
                embedding = generate_embedding(client, sentence)
                insert_document(cur, conn, sentence, embedding)
            except Exception:
                logging.warning("⚠️ Skipped sentence due to error: %s", sentence)

    finally:
        cur.close()
        conn.close()
        logging.info("🔒 Database connection closed.")


if __name__ == "__main__":
    main()
