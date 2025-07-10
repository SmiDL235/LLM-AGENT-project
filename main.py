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
from functions.run_python import schema_run_python, run_python_file
from functions.write_file import schema_write_file, write_file


def main():
	system_prompt = """
	You are a helpful AI coding agent.

	When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

	- List files and directories
	
	- Read file contents

	- Execute Python files with optional arguments

	- Write pr overwrite files

	All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
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
	
	function_call_list = {
		"get_files_info": get_files_info,
		"get_file_content": get_file_content,
		"run_python_file": run_python_file,
		"write_file": write_file,
	}
	
	if response.function_calls:
		for function_call_part in response.function_calls:
			function_name = function_call_part.name
			function_args = function_call_part.args
			if function_name in function_call_list:
				print(f"Function name: {function_name}")
				print(f"Function args: {function_args}")
				
				function_args['working_directory'] = os.getcwd()
				result = function_call_list[function_name](**function_args)
				print(result)


	else:
		print(response.text)

	if "--verbose" in sys.argv:

		print("User prompt:", user_prompt)
		print("Prompt tokens:", response.usage_metadata.prompt_token_count)
		print("Response tokens:", response.usage_metadata.candidates_token_count)

if __name__ == "__main__":
	main()
