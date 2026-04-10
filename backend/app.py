# ── Summarize AI — Flask Server ──────────────────────────────
# POST /api/summarize → receives text, returns structured summary
# ─────────────────────────────────────────────────────────────

import os
import uuid
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from sumai import run_summarizer

# ── Paths (absolute, so they work in debug mode too) ─────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")

# ── App Setup ────────────────────────────────────────────────
app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")
CORS(app)


# ── Route: Serve Frontend ────────────────────────────────────
@app.route("/")
def serve_frontend():
    """GET / → serves the frontend HTML page."""
    return send_from_directory(FRONTEND_DIR, "index.html")


# ── Route: Summarize API ─────────────────────────────────────
@app.route("/api/summarize", methods=["POST"])
def summarize():
    """
    POST /api/summarize
    Body: { "text": "...", "thread_id": "optional" }
    Returns: structured summary JSON
    """
    data = request.get_json()

    # Validate input
    if not data or not data.get("text"):
        return jsonify({"error": "No text provided"}), 400

    text = data["text"].strip()
    if len(text) < 10:
        return jsonify({"error": "Text too short (min 10 characters)"}), 400

    # Use provided thread_id or generate a new one
    thread_id = data.get("thread_id", str(uuid.uuid4()))

    # Run the LangGraph summarizer
    result = run_summarizer(text, thread_id=thread_id)

    if "error" in result:
        return jsonify({"error": result["error"]}), 500

    # Return structured response
    return jsonify({
        "success": True,
        "thread_id": thread_id,
        "data": result
    })


# ── Route: Health Check ──────────────────────────────────────
@app.route("/api/health", methods=["GET"])
def health():
    """GET /api/health → confirms server is running."""
    return jsonify({"status": "ok", "service": "Summarize AI"})


# ── Start Server ─────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print("🚀 Summarize AI Server")
    print("📡 API:      http://localhost:5000/api/summarize")
    print("🌐 Frontend: http://localhost:5000")
    print("💊 Health:   http://localhost:5000/api/health")
    print("=" * 50)
    app.run(debug=True, host="0.0.0.0", port=5000)
