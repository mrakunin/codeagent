import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import llm_model
from config import system_prompt
from config import available_functions
from call_function import call_function


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

    for _ in range(20):
        response = client.models.generate_content(
            model=llm_model,
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
                temperature=0,
            ),
        )
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        if response.usage_metadata is None:
            raise RuntimeError("No usage metadata: probebly failed API request")

        for candidate in response.candidates:
            messages.append(candidate.content)

        # print functions calls if available
        if response.function_calls is None:
            print(response.text)
            return
        else:
            function_results = []

            for call in response.function_calls:
                result = call_function(call)

                if result.parts is None:
                    raise Exception("Error: parts field is missing")
                if result.parts[0].function_response is None:
                    raise Exception("Error: function_response field is missing")
                if result.parts[0].function_response.response is None:
                    raise Exception("Error: response field is missing")

                function_results.append(result.parts[0])

                if args.verbose:
                    print(f"-> {result.parts[0].function_response.response}")

            messages.append(types.Content(role="user", parts=function_results))

    # we reached the maximum iteration count
    print("Error: Reched the maximum number of iterations")
    exit(1)


if __name__ == "__main__":
    main()
