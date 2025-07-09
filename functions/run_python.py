import os
import subprocess
from subprocess import TimeoutExpired

def run_python_file(working_directory, file_path):
	try:
		abs_working = os.path.abspath(working_directory)
		abs_target = os.path.abspath(os.path.join(working_directory, file_path  or ""))

		if not abs_target.startswith(abs_working):
			return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
		if not os.path.isfile(abs_target):
			return f'Error: File "{file_path}" not found'
		if not abs_target.endswith(".py"):
			return f'Error: "{abs_target}" is not a Python file'


		result = subprocess.run(["python3", abs_target], cwd=abs_working, timeout=30, capture_output=True, )
		outer_parts = []
		if result.stdout:
			outer_parts.append(f'STDOUT:{result.stdout.decode("utf-8")}')
		if result.stderr:
			outer_parts.append(f'STDERR:{result.stderr.decode("utf-8")}')
		if result.returncode != 0:
			outer_parts.append(f'Process exited with code "{result.returncode}"')
		if not outer_parts and result.returncode==0:
			return "No output produced"
		return "\n".join(outer_parts)


	except TimeoutExpired as e:
		return f"Error: executing Python file: {e}"
