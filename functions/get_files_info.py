import os


def get_files_info(working_directory, directory=None):
	try:
		abs_working = os.path.abspath(working_directory)
		abs_target = os.path.abspath(os.path.join(working_directory, directory or ""))

		if not abs_target.startswith(abs_working):
			return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
		if not os.path.isdir(abs_target):
			return f'Error: "{directory}" is not a directory'
		lines = []
		for item_name in sorted(os.listdir(abs_target)):
			item_path = os.path.join(abs_target, item_name)
			line = f'- {item_name}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}'
			lines.append(line)
		return '\n'.join(lines)
	except Exception as e:
		return f"Error: {str(e)}"
		
		
