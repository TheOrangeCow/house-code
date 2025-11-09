from flask import Flask, request, jsonify, render_template
import requests, uuid, os
from flask_cors import CORS
 

app = Flask(__name__)
CORS(app)
sessions = {}

@app.route("/")
def home():
    return "Render Code Runner API is live!"

@app.route("/run", methods=["POST"])
def run_code():
    data = request.get_json()
    code = data.get("code", "")

    # Create unique session
    sid = uuid.uuid4().hex

    # Execute safely through Piston API
    res = requests.post(
        "https://emkc.org/api/v2/piston/execute",
        json={"language": "python3", "source": code}
    )

    result = res.json()
    output = result.get("output", "")
    sessions[sid] = {"code": code, "output": output}

    return jsonify({
        "session_url": f"/env/{sid}",
        "output": output
    })

@app.route("/env/<sid>")
def env_view(sid):
    session = sessions.get(sid)
    if not session:
        return "Session not found or expired", 404
    return render_template("env.html", code=session["code"], output=session["output"])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
