import os
import sys

from constant import COST_PER_1K_INPUT, COST_PER_1K_OUTPUT, MODEL_NAME
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain_openai import ChatOpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("❌ No API key found in .env file.")
    sys.exit(1)

llm = ChatOpenAI(model=MODEL_NAME, api_key=api_key)

# Define prompt
prompt = ChatPromptTemplate.from_messages([("user", "{user_query}")])

# Define parser
parser = StrOutputParser()

# Build chain with LCEL pipe syntax
chain = prompt | llm | parser


def send_query_to_model(user_query: str):
    """
    Send a user query through LangChain pipeline and return response + token cost.
    """
    try:
        response = llm.invoke([{"role": "user", "content": user_query}])
        reply = response.content.strip()

        usage = response.response_metadata.get("token_usage", {})
        prompt_tokens = usage.get("prompt_tokens", 0)
        completion_tokens = usage.get("completion_tokens", 0)
        total_tokens = prompt_tokens + completion_tokens

        # Calculate cost (input + output separately)
        cost = (prompt_tokens / 1000) * COST_PER_1K_INPUT + (
            completion_tokens / 1000
        ) * COST_PER_1K_OUTPUT

        return reply, total_tokens, cost

    except Exception as e:
        raise RuntimeError(f"⚠️ Error while sending query: {e}")


def main():
    """
    Interactive chat session using LangChain pipeline.
    """
    total_tokens_accum = 0
    total_cost_accum = 0

    print(f"💬 Chat with {MODEL_NAME} (LangChain)! Type 'exit' to quit.\n")

    while True:
        try:
            user_query = input("You: ")
            if user_query.lower() == "exit":
                print("\n👋 Exiting chat...")
                print(f"Total tokens used: {total_tokens_accum}")
                print(f"Total cost: ${total_cost_accum:.5f} USD")
                break

            reply = chain.invoke({"user_query": user_query})

            _, tokens, cost = send_query_to_model(user_query)

            total_tokens_accum += tokens
            total_cost_accum += cost

            print(f"\n{MODEL_NAME}: {reply}")
            print(f"(Tokens this request: {tokens}, Approx. cost: ${cost:.5f} USD)\n")

        except KeyboardInterrupt:
            print("\n\n👋 Exiting chat (Ctrl+C pressed)...")
            break
        except Exception as e:
            print(f"⚠️ Error: {e}")


if __name__ == "__main__":
    main()
