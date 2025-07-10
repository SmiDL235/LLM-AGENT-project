

def call_function(function_call_part, verbose=False):
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
