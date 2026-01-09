import os
from dotenv import load_dotenv
from google import genai

llm_model = "gemini-2.5-flash"
llm_request = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("Could not read GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(model=llm_model, contents=llm_request)
    if response.usage_metadata is None:
        raise RuntimeError("No usage metadate: probebly failed API request")
    print(
        f"Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}"
    )
    print(response.text)


if __name__ == "__main__":
    main()
