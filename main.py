from flask import Flask, request, jsonify
import hashlib
from datetime import datetime

app = Flask(__name__)

SECRET = "Vm8Lk7Uj2JmsjCPVPVjrLa7zgfx3uz9E"

keys = {
    "TESTKEY": {"plan": "daily", "EXP": "2099-12-31"}
}

@app.route("/")
def home():
    return "✅ Loader Server is Running"

@app.route("/public/connect", methods=["POST"])
def connect():
    user_key = request.form.get("user_key")
    serial = request.form.get("serial")

    if not user_key or not serial:
        return jsonify({"status": False, "reason": "Missing parameters"})

    key_data = keys.get(user_key)
    if not key_data:
        return jsonify({"status": False, "reason": "Invalid key"})

    exp_date = datetime.strptime(key_data["EXP"], "%Y-%m-%d")
    if datetime.now() > exp_date:
        return jsonify({"status": False, "reason": "Key expired"})

    token_string = f"PUBG-{user_key}-{serial}-{SECRET}"
    token = hashlib.md5(token_string.encode()).hexdigest()

    return jsonify({
        "status": True,
        "data": {
            "token": token,
            "EXP": key_data["EXP"],
            "rng": int(datetime.now().timestamp())
        }
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
