"""Parse dataset version URL from notification payload.

The payload is a JSON file that Valohai sends to the step.
For local testing, you can use the following command:
python parse-notification.py --payload PAYLOAD_FILE
"""

import argparse
import json
import valohai

# --- for local testing: get the payload from the command line ---

parser = argparse.ArgumentParser(
    description="Parse dataset version URL from notification payload."
)
parser.add_argument("--payload", type=str, required=False, help="Datum payload file")
args = parser.parse_args()

# ---

input_file = valohai.inputs("payload").path() or args.payload
print(f"Reading payload from {input_file}")

with open(args.payload or valohai.inputs("payload").path()) as file:
    payload = json.load(file)

print("Got this data from the input:")
print(json.dumps(payload, indent=2))

dataset_version_uri = payload["data"]["version"]["uri"]
print(f"{dataset_version_uri=}")
