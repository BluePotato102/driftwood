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
import aes_encryptor_temp as aes_encryptor

CONFIG_FILE = "config.json"
HASHED_CONFIG_FILE = "hashed_answers.json"

with open(CONFIG_FILE, "r") as f:
    data = json.load(f)
    print(data)

for section in data.get("sections", []):
    for q in section.get("questions", []):
        answer = q.pop("answer", None)
        if answer:
            salt = os.urandom(16).hex()
            q["hash"] = hashlib.sha256((answer + salt).encode()).hexdigest() + ":" + salt

with open(HASHED_CONFIG_FILE, "w") as f: # this is only here for testing now as it doesnt actually matter
    json.dump(data, f, indent=2)

aes_encryptor.encrypt(data)