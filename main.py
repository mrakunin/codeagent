import os
import argparse
from dotenv import load_dotenv
from google import genai

llm_model = "gemini-2.5-flash"


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("Could not read GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="AI agent for code generation")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()

    response = client.models.generate_content(model=llm_model, contents=args.user_prompt)
    if response.usage_metadata is None:
        raise RuntimeError("No usage metadate: probebly failed API request")
    print(
        f"Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}"
    )
    print(response.text)


if __name__ == "__main__":
    main()
