# to be (probably) delted

#!/usr/bin/env python3

# Step 1: check for requirments

# Step 2: check if config.json is valid

# Step 3: create hashes from config

# Step 3.5: create venv

# Step 4: using hashes launch the app.py and keep it running

# Step 5: shred all these files

#nvm i need a minimal version for testing on windows, it ONLY creates the hash file

import json, hashlib, os

CONFIG_FILE = "config.json"
HASHED_CONFIG_FILE = "hashed_answers.json"

with open(CONFIG_FILE, "r") as f:
    data = json.load(f)

for section in data.get("sections", []):
    for q in section.get("questions", []):
        # replace answer with empty string
        answer = q["answer"]
        q["answer"] = ""

        salt = os.urandom(16).hex()

        # hash answer
        if answer:
            q["hash"] = hashlib.sha256((answer + salt).encode()).hexdigest() + ":" + salt

        # insert try count
        if "tries" not in q:
            q["tries"] = 0

with open(HASHED_CONFIG_FILE, "w") as f:
    json.dump(data, f, indent=2)
