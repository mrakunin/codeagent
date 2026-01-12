import os
from google.genai import types


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="writes the specified content to a file relative to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to the file to write to, relative to the working directory"
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file"
            )
        },
        required=["file_path", "content"]
    )
)


def write_file(working_directory, file_path, content):
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
    if os.path.commonpath([working_dir_abs, target_file]) != working_dir_abs:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if os.path.isdir(target_file):
        return f'Error: Cannot write to "{file_path}" as it is a directory'

    # make sure target_dir exists
    target_dir = os.path.dirname(target_file)
    os.makedirs(name=target_dir, exist_ok=True)

    try:
        with open(target_file, "w") as f:
            f.write(content)
    except IOError:
        return f'Error: Cannot write to file: "{file_path}"'

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
