import os
from google.genai import types


def get_file_content(working_directory, file_path):
	try:
		abs_working = os.path.abspath(working_directory)
		abs_target = os.path.abspath(os.path.join(working_directory, file_path or ""))

		if not abs_target.startswith(abs_working):
			return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
		if not os.path.isfile(abs_target):
			return f'Error: File not found or is not a regular file: "{file_path}"'
		
		MAX_CHARS = 10000
		file_size = os.path.getsize(abs_target)

		with open(abs_target, "r") as f:
			file_content_string = f.read(MAX_CHARS)
		if file_size > MAX_CHARS:
			return (file_content_string + f'[...File "{file_path}" truncated at 10000 characters]')	
		return file_content_string

	except Exception as e:
		return f"Error: {str(e)}"




schema_get_file_content = types.FunctionDeclaration(
	name="get_file_content",
	description="Read file contents, constrained to the working directory.",
	parameters=types.Schema(
		type=types.Type.OBJECT,
		properties={
			"file_path": types.Schema(
			type=types.Type.STRING,
				description="Read the content of a given file, relative to the working directory. If not provided, ask what file you need to read.",
			),
		},
	),
)
