import os
from google.genai import types


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            )
        },
    ),
)


def get_files_info(working_directory, directory="."):
    if directory == ".":
        result = f"Result for current directory:"
    else:
        result = f"Result for '{directory}':"

    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
    if os.path.commonpath([working_dir_abs, target_dir]) != working_dir_abs:
        return f'{result}\n    Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.exists(target_dir):
        return f'{result}\n    Error: "{directory}" does not exist'

    if not os.path.isdir(target_dir):
        return f'{result}\n    Error: "{directory}" is not a directory'


    dir_list = os.listdir(target_dir)

    for item in dir_list:
        new_target = f'{target_dir}/{item}'
        target_name = item
        target_size = os.path.getsize(new_target)
        target_isdir = os.path.isdir(new_target)

        result += f'\n  - {target_name}: file_size={target_size} bytes, is_dir={target_isdir}'

    return result
