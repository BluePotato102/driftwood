from flask import Flask, render_template, jsonify, request
import json, hashlib

app = Flask(__name__)

with open("hashed_answers.json") as f:
    HASHED_ANSWERS = json.load(f)

TITLE = HASHED_ANSWERS.get("title", "Driftwood")

@app.route("/")
def home():
    return render_template("index.html", title=TITLE)

@app.route("/readme")
def readme():
    return render_template("readme.html", title=TITLE)

@app.route("/flags")
def flags():
    return render_template("flags.html", sections=HASHED_ANSWERS["sections"], title=TITLE)

@app.route("/results")
def results():
    return render_template("results.html", title=TITLE)

@app.route("/config")
def get_config():
    return jsonify(HASHED_ANSWERS)

@app.route("/submit_flag", methods=["POST"])
def submit_flag():
    data = request.get_json()
    section_name = data.get("section")
    index = int(data.get("index"))
    user_flag = data.get("flag", "").strip()

    section = next((s for s in HASHED_ANSWERS["sections"] if s["name"] == section_name), None)
    if not section or index >= len(section["questions"]):
        return jsonify(success=False, message="Invalid question.")

    question = section["questions"][index]
    stored_hash, salt = question["hash"].split(":")
    user_hash = hashlib.sha256((user_flag + salt).encode()).hexdigest()

    question["tries"] = question.get("tries", 0) + 1
    max_tries = HASHED_ANSWERS.get("maxTries", "Infinity")

    if user_hash == stored_hash:
        question["answer"] = user_flag
        success = True
        message = "Correct!"
    else:
        success = False
        message = "Incorrect."

    with open("hashed_answers.json", "w") as f:
        json.dump(HASHED_ANSWERS, f, indent=2)

    return jsonify({
        "success": success,
        "message": message,
        "tries": question["tries"],
        "maxTries": max_tries
    })







if __name__ == "__main__":
    app.run(debug=True)