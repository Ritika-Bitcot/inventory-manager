# Model name
MODEL_NAME = "gpt-4o-mini"
MODEL_NAME_EMBEDDING = "text-embedding-3-small"

# Pricing
COST_PER_1K_INPUT = 0.000150  # $0.15 per 1M input tokens
COST_PER_1K_OUTPUT = 0.000600  # $0.60 per 1M output tokens
TOKENS_PER_UNIT = 1000

# Database
PGVECTOR_COLLECTION_NAME = "product_embeddings"

# Text splitting
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

RAG_PROMPT_TEMPLATE: str = """
You are a helpful assistant. Use the provided context to answer the question.

Context:
{context}

Question:
{question}

Answer:
"""
