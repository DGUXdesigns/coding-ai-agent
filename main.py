import argparse
import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import available_functions, call_function
from prompts import system_prompt


def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")

    for _ in range(20):
        try:
            final_response = generate_content(client, messages, args.verbose)
            if final_response:
                print("Final response:")
                print(final_response)
                return
        except Exception as e:
            print(f"Error in generate_content: {e}")

    print("Maximum iterations (20) reached")
    sys.exit(1)


def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
        ),
        contents=messages,
    )

    if not response.usage_metadata:
        raise RuntimeError("Something went wrong, no usage metadata available")

    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if response.candidates:
        for candidate in response.candidates:
            if candidate.content:
                messages.append(candidate.content)

    if not response.function_calls:
        return response.text

    function_results = []
    for function_call in response.function_calls:
        function_call_result = call_function(function_call, verbose)

        if not function_call_result.parts:
            raise RuntimeError("Function call returned no parts")

        part = function_call_result.parts[0]

        if not part.function_response:
            raise RuntimeError("Missing function_response in function result")

        if not part.function_response.response:
            raise RuntimeError("Function response was None")

        function_results.append(part)

        if verbose:
            print(f"-> {part.function_response.response}")

    messages.append(
        types.Content(
            role="user",
            parts=function_results,
        )
    )


if __name__ == "__main__":
    main()
