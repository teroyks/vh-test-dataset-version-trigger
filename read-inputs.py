"""Loop through all inputs given to the current step."""

import valohai

print("I have inputs!")

inputs = {
    "dataset": "",
}

valohai.prepare(step="list-inputs", default_inputs=inputs)

for file_path in valohai.inputs("dataset").paths():
    with open(file_path, "r") as file:
        line_count = len(file.readlines())
    print(f"Number of lines in {file_path}: {line_count}")
