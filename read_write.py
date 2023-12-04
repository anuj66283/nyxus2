import json
import hashlib
import base64


def read_data(file):
    with open(file, "r") as f:
        try:
            return json.load(f)
        except:
            return {}


def write_data(obj, file):
    with open(file, "w") as f:
        json.dump(obj, f)


def create_unique(*args):
    combined_string = "_".join(args)
    hashed = hashlib.sha256(combined_string.encode()).digest()
    encoded_id = base64.urlsafe_b64encode(hashed)[:15].decode("utf-8")
    return encoded_id
