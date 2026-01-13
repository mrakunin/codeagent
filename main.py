import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import llm_model
from config import system_prompt
from config import available_functions


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("Could not read GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="AI agent for code generation")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    response = client.models.generate_content(
        model=llm_model,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt, temperature=0
        ),
    )
    if response.usage_metadata is None:
        raise RuntimeError("No usage metadata: probebly failed API request")

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    # print functions calls if available
    if response.function_calls is None:
        print(response.text)
    else:
        for call in response.function_calls:
            print(f"Calling function: {call.name}({call.args})")


if __name__ == "__main__":
    main()
