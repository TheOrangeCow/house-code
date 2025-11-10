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

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import requests, uuid, os

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Render Code Runner API is live!"

@app.route("/run", methods=["POST"])
def run_code():
    data = request.get_json()
    code = data.get("code", "")

    res = requests.post(
        "https://emkc.org/api/v2/piston/execute",
        json={"language": "python3", "source": code}
    )

    result = res.json()
    output = result.get("output", "")

    sid = uuid.uuid4().hex

    html = f"""
    <!DOCTYPE html>
    <html lang='en'>
    <head>
      <meta charset='UTF-8'>
      <title>Environment {sid}</title>
      <style>
        body {{ font-family: monospace; background: #111; color: #eee; padding: 20px; }}
        h1 {{ color: #66d9ef; }}
        pre {{ background: #1e1e1e; padding: 15px; border-radius: 8px; white-space: pre-wrap; }}
      </style>
    </head>
    <body>
      <h1>Python Execution Environment</h1>
      <div><h3>Your Code:</h3><pre>{code}</pre></div>
      <div><h3>Output:</h3><pre>{output}</pre></div>
    </body>
    </html>
    """

    return html



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
