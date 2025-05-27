#!/bin/bash

CONFIG_FILE="config.json"
HASHED_CONFIG_FILE="hashed_config.json"

# Step 0: requiure root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root: \`sudo ./release.sh\`"
  exit 1
fi

# Step 1: check for python version and install dependencies
echo "Checking python version"
if ! command -v python3 &>/dev/null; then
    echo "Python not installed. Aborting..."
    exit 1
fi

echo "Installing dependenices"
pip install --upgrade pip
pip install -r requirements.txt

# Step 2: check if config.json is valid
echo "Validating config.json"
if ! python3 -c "import json; json.load(open('$CONFIG_FILE'))" 2>/dev/null; then
    echo "[!] config.json is invalid JSON. Aborting..."
    exit 1
fi

# Step 3: create hashes from config
echo "Hashing answers"
python3 <<EOF
import json, hashlib, os

with open($CONFIG_FILE, "r") as f:
    data = json.load(f)

for section in data.get("sections", []):
    for q in section.get("questions", []):
        answer = q.pop("answer", None)
        if answer:
            salt = os.urandom(16).hex()
            q["hash"] = hashlib.sha256((answer + salt).encode()).hexdigest() + ":" + salt

with open($HASHED_CONFIG_FILE, "w") as f:
    json.dump(data, f, indent=2)
EOF

# Step 4: launch the app.py and keep it running
cat > "/etc/systemd/system/driftwood.service" <<EOL
[Unit]
Description=Boeing Practice Engine
After=network.target

[Service]
ExecStart=$(which python3) $(pwd)/app.py
WorkingDirectory=$(pwd)
Restart=always
User=$SUDO_USER
Environment=FLASK_ENV=production

[Install]
WantedBy=multi-user.target
EOL

echo "Enabling and starting service"
systemctl daemon-reload
systemctl enable driftwood.service
systemctl start driftwood.service

# Step 5: shred all these files
echo "Shredding originals"
# shred -u "$CONFIG_FILE" # commented out for testing purpouses
# not sure if we need to shred anything else