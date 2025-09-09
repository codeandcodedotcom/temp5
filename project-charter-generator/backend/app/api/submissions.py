from flask import Blueprint, jsonify, current_app
from app.services.storage import list_submissions

bp = Blueprint("submissions", __name__)

@bp.route("/submissions", methods=["GET"])
def get_submissions():
    """
    Return recent stored submissions for demo/admin use.
    """
    try:
        rows = list_submissions(limit=100)
        return jsonify({"submissions": rows}), 200
    except Exception:
        current_app.logger.exception("Failed to read submissions")
        return jsonify({"error": "Failed to read submissions"}), 500


# curl -X POST http://127.0.0.1:5000/api/generation/ask -H "Content-Type: application/json" -d "{\"project_name\":\"CRM Upgrade Initiative\",\"sponsor\":\"Alice Smith\",\"answers\":[{\"id\":\"q1\",\"question\":\"Do you have approved budget?\",\"answer\":\"Yes\",\"score\":5}],\"additional_context\":\"Demo run\"}"

