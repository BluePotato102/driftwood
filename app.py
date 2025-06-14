from flask import Flask, render_template, jsonify, request
import json, hashlib
# import aes_encryptor
import aes_encryptor_temp as aes_encryptor

app = Flask(__name__)

with open("hashed_answers.json") as f:
    HASHED_ANSWERS = json.load(f)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/flags")
def flags():
    return render_template("flags.html", sections=HASHED_ANSWERS["sections"])

@app.route("/results")
def results():
    return render_template("results.html")

@app.route("/config")
def get_config():
    return jsonify(HASHED_ANSWERS)

@app.route("/submit_flag", methods=["POST"])
def submit_flag():
    data = request.get_json()
    section_name = data.get("section")
    index = int(data.get("index"))
    user_flag = data.get("flag", "").strip()

    try:
        all_data = aes_encryptor.decrypt()
    except Exception as e:
        return jsonify(success=False, message=f"Error decrypting: {str(e)}")

    section = next((s for s in all_data.get("sections", []) if s.get("name") == section_name), None)
    if not section or index >= len(section.get("questions", [])):
        return jsonify(success=False, message="Invalid question.")

    question = section["questions"][index]
    stored_hash, salt = question.get("hash", "").split(":")
    user_hash = hashlib.sha256((user_flag + salt).encode()).hexdigest()

    if user_hash == stored_hash:
        return jsonify(success=True, message="Correct!")
    else:
        return jsonify(success=False, message="Incorrect.")

if __name__ == "__main__":
    app.run(debug=True)