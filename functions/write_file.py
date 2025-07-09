import os

def write_file(working_directory, file_path, content):
	try:
		abs_working = os.path.abspath(working_directory)
		abs_target = os.path.abspath(os.path.join(working_directory, file_path or ""))
		
		if not abs_target.startswith(abs_working):
			return f'Error: Cannot write to "{abs_target}" as it is outside tghe permitted working directory'
		
		if os.path.exists(abs_target) == False:
			dir_name = os.path.dirname(abs_target)
			os.path.makedirs(dir_name)
		with open(abs_target, "w") as f:
			f.write(content)
		return f'Successfully wrote to "{abs_target}" ({len(content)} characters written)'
	except Exception as e:
		return f"Error: {str(e)}"
	
