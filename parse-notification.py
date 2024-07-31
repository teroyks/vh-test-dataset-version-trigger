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

# notification payload is provided in a Valohai input file
input_file = valohai.inputs("payload").path()

# --- local testing only: get the payload from the command line ---
input_file = input_file or args.payload

# get the json "payload" content from the input file
with open(input_file) as file:
    payload = json.load(file)

# retrieve the new dataset version URI from the payload
dataset_version_uri = payload["data"]["version"]["uri"]

# output the URI as execution metadata
# this will be available to the next step

print(json.dumps({"dataset": dataset_version_uri}))
