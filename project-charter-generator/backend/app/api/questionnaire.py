from flask import Blueprint, jsonify, current_app
import os, json

bp = Blueprint("questionnaire", __name__)

@bp.route("/questionnaire", methods=["GET"])
def get_questionnaire():
    """
    Return the questionnaire JSON used by the frontend.
    """
    candidates = [
        os.path.join(os.getcwd(), "dev_fixtures", "questions_structured.json"),
        os.path.join(os.path.dirname(__file__), "..", "dev_fixtures", "questions_structured.json"),
        os.path.join(os.path.dirname(__file__), "..", "..", "dev_fixtures", "questions_structured.json"),
        os.path.join(os.getcwd(), "app", "dev_fixtures", "questions_structured.json"),
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as fh:
                    data = json.load(fh)
                current_app.logger.info(f"Loaded questionnaire from {path}")
                return jsonify(data), 200
            except Exception:
                current_app.logger.exception("Failed to load questionnaire JSON")
                return jsonify({"error": "Failed to load questionnaire"}), 500

    current_app.logger.error("Questionnaire JSON not found in expected locations: " + ", ".join(candidates))
    return jsonify({"error": "Questionnaire not found"}), 404
