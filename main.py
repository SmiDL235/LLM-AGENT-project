import sys
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

from google import genai

client = genai.Client(api_key=api_key)

from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python import schema_run_python, run_python
from functions.write_file import schema_write_file, write_file
from functions.call_function import call_function


def main():
	system_prompt = """
	You are a helpful AI coding agent with access to file system tools.

	You MUST use the available functions to complete tasks. When a user asks a question:

	1. Use get_files_info() to list files and directories
	2. Use get_file_content() to read file contents
	3. Use run_python() to execute Python files
	4. Use write_file() to create or modify files

	Do NOT ask the user for file paths or information you can get yourself using these functions.

	All paths should be relative to the working directory. The working directory is automatically injected for security.

	Always start by using get_files_info() to see what files are available, then use other functions as needed.

	When analyzing images of asteroids, remember that asteroids are generally irregular shapes.
	They are not typically triangles or other simple geometric shapes.
	Focus on identifying overall shape characteristics and surface features.
	"""
	available_functions= types.Tool(
		function_declarations=[
			schema_get_files_info,
			schema_get_file_content,
			schema_run_python,
			schema_write_file,
		]
	)
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
		config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
	)

	verbose = "--verbose" in sys.argv


	for i in range(20):
		try:
			response = client.models.generate_content(
				model = "gemini-2.0-flash-001" ,
				contents=messages,
				config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
			)
			for candidate in response.candidates:
				messages.append(candidate.content)

			# Look for function calls in the parts
			function_calls_found = False
			for candidate in response.candidates:
				for part in candidate.content.parts:
					if hasattr(part, 'function_call') and part.function_call:
						function_calls_found = True
						
						

						function_response = call_function(part.function_call, verbose=verbose)
						if (
							not function_response.parts
							or not hasattr(function_response.parts[0], "function_response")
							or not getattr(function_response.parts[0].function_response, "response", None)
						):
							raise Exception("No function_response.response found!")
						print(f"-> {function_response.parts[0].function_response.response}")
						messages.append(function_response)
			if not function_calls_found:
				# No function calls, this is the final response
				print("Final response:")
				print(response.text)
				break




		except Exception as e:
			print(f"Error: {e}")
			break


	if "--verbose" in sys.argv:

		print("User prompt:", user_prompt)
		print("Prompt tokens:", response.usage_metadata.prompt_token_count)
		print("Response tokens:", response.usage_metadata.candidates_token_count)

if __name__ == "__main__":
	main()
