from flask import Blueprint, jsonify
from app.utils.logger import get_logger

bp = Blueprint("health", __name__)
logger = get_logger(__name__)

@bp.route("/health", methods=["GET"])
def health():
    """
    Liveness probe - returns 200 if the backend process is alive.
    """
    logger.info("Health check OK")
    return jsonify({"status": "ok"}), 200
