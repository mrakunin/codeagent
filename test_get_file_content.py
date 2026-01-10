from config import MAX_CHARS
from functions.get_file_content import get_file_content

expected_message = f'[...File "lorem.txt" truncated at {MAX_CHARS} characters]'

content = get_file_content("calculator", "lorem.txt")
if content[MAX_CHARS:] == expected_message:
    print('Success: lorem test did pass')
else:
    print('Error: lorem test did not pass')

print(get_file_content("calculator", "main.py"))
print(get_file_content("calculator", "pkg/calculator.py"))
print(get_file_content("calculator", "/bin/cat"))
print(get_file_content("calculator", "pkg/does_not_exist.py"))

