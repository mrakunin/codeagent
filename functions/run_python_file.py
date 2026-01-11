import os
import subprocess


def run_python_file(working_directory, file_path, args=None):
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
    if os.path.commonpath([working_dir_abs, target_file]) != working_dir_abs:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    print(f"target_file = {target_file}")
    if not os.path.isfile(target_file):
        return f'Error: "{file_path}" does not exist or is not a regular file'

    if file_path[-3:] != ".py":
        return f'Error: "{file_path}" is not a Python file'

    command = ["python", target_file]
    if args is not None:
        command.extend(args)

    try:
        result = subprocess.run(
            command, cwd=working_directory, capture_output=True, text=True, timeout=30
        )
    except Exception as e:
        f"Error: executing Python file: {e}"

    return_string = ""
    if result.returncode != 0:
        return_string += "Process ecited with code X"

    if result.stdout == "" and result.stdout == "":
        return_string += "\nNo output produced"

    if result.stdout != "":
        return_string += f"\nSTDOUT:{result.stdout}"

    if result.stderr != "":
        return_string += f"\nSTDERR:{result.stderr}"

    return return_string
