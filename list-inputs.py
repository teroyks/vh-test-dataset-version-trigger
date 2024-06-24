"""List all inputs given to the current step."""

import valohai

valohai.prepare(step="list-inputs")

print("I have inputs!")

inputs = {
    "dataset": "",
}

valohai.prepare(step="list-inputs", default_inputs=inputs)

for file_path in valohai.inputs("dataset").paths():
    print(file_path)
