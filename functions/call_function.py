from google.genai import types
from .get_files_info import get_files_info
from .get_file_content import get_file_content
from .run_python import run_python
from .write_file import write_file 

def call_function(function_call_part, verbose=False):
	function_call_list = {
		"get_files_info": get_files_info,
		"get_file_content": get_file_content,
		"run_python": run_python,
		"write_file": write_file,
	}


	function_name = function_call_part.name
	function_args = dict(function_call_part.args)
	function_args["working_directory"] = "./calculator"
	if function_name not in function_call_list:
		return types.Content(
			role="tool",
			parts=[
				types.Part.from_function_response(
					name=function_name,
					response={"error": f"Unknown function: {function_name}"},
				)
			],
		)
	else:
		if verbose:
			print(f"Calling function: {function_name}({function_args})")
		function_result = function_call_list[function_name](**function_args)
		if verbose:
			print(f"-> {function_result}")
		return types.Content(
			role="tool",
			parts=[
				types.Part.from_function_response(
					name=function_name,
					response={"result": function_result},
				)
			],
		)
