import os
import sys
from typing import Tuple

from constant import COST_PER_1K_INPUT, COST_PER_1K_OUTPUT, MODEL_NAME
from dotenv import load_dotenv
from openai import APIError, AuthenticationError, OpenAI, OpenAIError, RateLimitError

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("❌ No API key found in .env file.")
    sys.exit(1)

client = OpenAI(api_key=api_key)


def send_query_to_model(user_query: str) -> Tuple[str, int, float]:
    """
    Send a user query to GPT and return the response, token usage, and cost.

    Args:
        user_query (str): The user's question or prompt.

    Returns:
        Tuple[str, int, float]: The reply, total tokens used, and approximate cost.

    Raises:
        OpenAIError: If the API call fails for any reason.
    """
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": user_query}],
        )

        reply = response.choices[0].message.content.strip()
        usage = response.usage

        prompt_tokens = usage.prompt_tokens
        completion_tokens = usage.completion_tokens
        total_tokens = usage.total_tokens

        # Calculate cost (input + output separately)
        cost = (prompt_tokens / 1000) * COST_PER_1K_INPUT + (
            completion_tokens / 1000
        ) * COST_PER_1K_OUTPUT

        return reply, total_tokens, cost

    except AuthenticationError:
        raise OpenAIError("Authentication failed. Please check your API key.")
    except RateLimitError:
        raise OpenAIError("Rate limit exceeded. Try again later.")
    except APIError as e:
        raise OpenAIError(f"API error occurred: {e}")
    except Exception as e:
        raise OpenAIError(f"Unexpected error: {e}")


def main() -> None:
    """
    Run an interactive chat session with GPT-4o-mini.
    Tracks total token usage and cost until the user exits.
    """
    total_tokens_accum = 0
    total_cost_accum = 0

    print(f"💬 Chat with {MODEL_NAME}! Type 'exit' to quit.\n")

    while True:
        try:
            user_query = input("You: ")
            if user_query.lower() == "exit":
                print("\n👋 Exiting chat...")
                print(f"Total tokens used: {total_tokens_accum}")
                print(f"Total cost: ${total_cost_accum:.5f} USD")
                break

            reply, tokens, cost = send_query_to_model(user_query)

            total_tokens_accum += tokens
            total_cost_accum += cost

            print(f"\n{MODEL_NAME}: {reply}")
            print(f"(Tokens this request: {tokens}, Approx. cost: ${cost:.5f} USD)\n")

        except OpenAIError as e:
            print(f"⚠️ Error: {e}")
        except KeyboardInterrupt:
            print("\n\n👋 Exiting chat (Ctrl+C pressed)...")
            break


if __name__ == "__main__":
    main()
