from flask import Flask, jsonify

APP_VERSION = "1.0"

app = Flask(__name__)


@app.get("/")
def index():
    return jsonify(message="Hello from CI/CD", version=APP_VERSION)


@app.get("/health")
def health():
    return jsonify(status="ok"), 200
