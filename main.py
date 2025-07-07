

import sys
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

from google import genai

client = genai.Client(api_key=api_key)

from google.genai import types


def main():
	if len(sys.argv) < 2:
		print("Error: no command line")
		sys.exit(1)
	user_prompt = sys.argv[1]
	messages = [
                 types.Content(role="user", parts=[types.Part(text=user_prompt)]),
	]
	response = client.models.generate_content(
		model = "gemini-2.0-flash-001" ,
		contents=messages,
		)
	
	print(response.text)
	
	if "--verbose" in sys.argv:

		print("User prompt:", user_prompt)
		print("Prompt tokens:", response.usage_metadata.prompt_token_count)
		print("Response tokens:", response.usage_metadata.candidates_token_count)

if __name__ == "__main__":
	main()
