# Week8/scripts/constant.py

# ==========================
# OpenAI Models
# ==========================
MODEL_NAME = "gpt-4o-mini"
MODEL_NAME_EMBEDDING = "sentence-transformers/all-MiniLM-L6-v2"
OPENAI_CHAT_MODEL = "gpt-4o-mini"
OPENAI_TEMPERATURE = 0.0

# ==========================
# Pricing
# ==========================
COST_PER_1K_INPUT = 0.000150
COST_PER_1K_OUTPUT = 0.000600
TOKENS_PER_UNIT = 1000

# ==========================
# Database
# ==========================
PGVECTOR_COLLECTION_NAME = "product_embeddings"

# ==========================
# Text Splitting
# ==========================
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# ==========================
# Cache Defaults
# ==========================
DEFAULT_CACHE_MODEL = "huggingface"
