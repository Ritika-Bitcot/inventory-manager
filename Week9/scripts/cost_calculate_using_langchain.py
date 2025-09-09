import os
import sys
from typing import Tuple

import requests
from constant import COST_PER_1K_INPUT, COST_PER_1K_OUTPUT, MODEL_NAME, TOKENS_PER_UNIT
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain_openai import ChatOpenAI
from openai import OpenAIError


def calculate_cost(prompt_tokens: int, completion_tokens: int) -> float:
    """
    Calculate the cost of tokens based on model pricing.

    Args:
        prompt_tokens (int): Number of input tokens.
        completion_tokens (int): Number of output tokens.

    Returns:
        float: The calculated cost in USD.
    """
    return (prompt_tokens / TOKENS_PER_UNIT) * COST_PER_1K_INPUT + (
        completion_tokens / TOKENS_PER_UNIT
    ) * COST_PER_1K_OUTPUT


def send_query_to_model(user_query: str, llm: ChatOpenAI) -> Tuple[str, int, float]:
    """
    Send a query to the model and return its response along with token usage and cost.

    Args:
        user_query (str): The user's input query.
        llm (ChatOpenAI): The language model instance to query.

    Returns:
        Tuple[str, int, float]:
            - reply (str): Model's textual response.
            - total_tokens (int): Total tokens consumed.
            - cost (float): Cost in USD.

    Raises:
        RuntimeError: If an API or unexpected error occurs.
    """
    try:
        response = llm.invoke([{"role": "user", "content": user_query}])
        reply: str = response.content.strip()

        usage: dict = response.response_metadata.get("token_usage", {})
        prompt_tokens: int = usage.get("prompt_tokens", 0)
        completion_tokens: int = usage.get("completion_tokens", 0)
        total_tokens: int = prompt_tokens + completion_tokens

        cost: float = calculate_cost(prompt_tokens, completion_tokens)
        return reply, total_tokens, cost

    except (OpenAIError, requests.exceptions.RequestException) as e:
        raise RuntimeError(f"⚠️ API request error: {e}")
    except Exception as e:
        raise RuntimeError(f"⚠️ Unexpected error: {e}")


def run_chat_session(llm: ChatOpenAI) -> None:
    """
    Run an interactive chat session with the model.
    Tracks cumulative tokens and cost until user exits.

    Args:
        llm (ChatOpenAI): The language model instance to use for chat.
    """
    # Build chain inside the function
    prompt = ChatPromptTemplate.from_messages([("user", "{user_query}")])
    parser = StrOutputParser()
    chain = prompt | llm | parser

    total_tokens_accum: int = 0
    total_cost_accum: float = 0.0

    print(f"💬 Chat with {MODEL_NAME} (LangChain)! Type 'exit' to quit.\n")

    while True:
        try:
            user_query: str = input("You: ")
            if user_query.lower() == "exit":
                print("\n👋 Exiting chat...")
                print(f"Total tokens used: {total_tokens_accum}")
                print(f"Total cost: ${total_cost_accum:.5f} USD")
                break

            reply: str = chain.invoke({"user_query": user_query})

            _, tokens, cost = send_query_to_model(user_query, llm)
            total_tokens_accum += tokens
            total_cost_accum += cost

            print(f"\n{MODEL_NAME}: {reply}")
            print(f"(Tokens this request: {tokens}, Approx. cost: ${cost:.5f} USD)\n")

        except KeyboardInterrupt:
            print("\n\n👋 Exiting chat (Ctrl+C pressed)...")
            break
        except Exception as e:
            print(f"⚠️ Error: {e}")


def main() -> None:
    """
    Main entry point for the program.
    Loads environment variables, initializes the model, and starts chat.
    """
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ No API key found in .env file.")
        sys.exit(1)

    llm = ChatOpenAI(model=MODEL_NAME, api_key=api_key)
    run_chat_session(llm)


if __name__ == "__main__":
    main()
