from flask import *
import json
import hashlib

app = Flask(__name__)

with open("config.json") as f:
    CONFIG = json.load(f)

@app.route("/")
def home():
    return render_template("index.html")

# ahhh flask

if __name__ == "__main__":
    app.run(debug=True)