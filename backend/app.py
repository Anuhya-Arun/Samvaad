
from flask import Flask, jsonify, request
from flask_cors import CORS

from chatbot import get_response, get_suggestions

app = Flask(__name__)
CORS(app)


@app.get("/api/health")
def health():
    return jsonify({
        "status": "ok",
        "app": "Samvaad"
    })


@app.post("/api/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "")

    if not isinstance(message, str) or not message.strip():
        return jsonify({
            "error": "Please enter a message."
        }), 400

    if len(message) > 1000:
        return jsonify({
            "error": "Message must be 1000 characters or fewer."
        }), 400

    answer = get_response(message)

    return jsonify({
        "reply": answer,
        "suggestions": answer["questions"]
    })


@app.get("/api/suggestions")
def suggestions():
    return jsonify({
        "suggestions": get_suggestions()
    })


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )
