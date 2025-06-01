from flask import Flask, render_template, jsonify, request
import json, hashlib

app = Flask(__name__)

with open("hashed_config.json") as f:
    HASHED_CONFIG = json.load(f)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/flags")
def flags():
    return render_template("flags.html", sections=HASHED_CONFIG["sections"])

@app.route("/results")
def results():
    return render_template("results.html")

@app.route("/config")
def get_config():
    return jsonify(HASHED_CONFIG)

@app.route("/submit_flag", methods=["POST"])
def submit_flag():
    data = request.get_json()
    section_name = data.get("section")
    index = int(data.get("index"))
    user_flag = data.get("flag", "").strip()

    section = next((s for s in HASHED_CONFIG["sections"] if s["name"] == section_name), None)
    if not section or index >= len(section["questions"]):
        return jsonify(success=False, message="Invalid question.")

    question = section["questions"][index]
    stored_hash, salt = question["hash"].split(":")
    user_hash = hashlib.sha256((user_flag + salt).encode()).hexdigest()

    if user_hash == stored_hash:
        return jsonify(success=True, message="Correct!")
    else:
        return jsonify(success=False, message="Incorrect.")

if __name__ == "__main__":
    app.run(debug=True)