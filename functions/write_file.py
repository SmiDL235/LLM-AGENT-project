import os
from google.genai import types


def write_file(working_directory, file_path, content):
	try:
		abs_working = os.path.abspath(working_directory)
		abs_target = os.path.abspath(os.path.join(working_directory, file_path or ""))
		
		if not abs_target.startswith(abs_working):
			return f'Error: Cannot write to "{abs_target}" as it is outside tghe permitted working directory'
		
		if os.path.exists(abs_target) == False:
			dir_name = os.path.dirname(abs_target)
			os.makedirs(dir_name, exist_ok=True)
		with open(abs_target, "w") as f:
			f.write(content)
		return f'Successfully wrote to "{abs_target}" ({len(content)} characters written)'
	except Exception as e:
		return f"Error: {str(e)}"



schema_write_file = types.FunctionDeclaration(
	name="write_file",
	description="Write or overwrite files, constrained to the working directory.",
	parameters=types.Schema(
		type=types.Type.OBJECT,
		properties={
			"file_path": types.Schema(
			type=types.Type.STRING,
				description="Write or overwrite the contents of a file, relative to the working directory. If not provided, ask which file to you need to write.",
			),
			"content": types.Schema(
				type=types.Type.STRING,
				description="The content to write to the file"
			)
		},
		required=["file_path", "content"]
	),
)	
