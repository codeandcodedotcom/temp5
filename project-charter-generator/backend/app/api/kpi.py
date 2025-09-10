# app/api/kpi.py
from flask import Blueprint, jsonify, request
from app.services import kpi_view
from app.utils.logger import get_logger

bp = Blueprint("kpi", __name__)
logger = get_logger(__name__)

@bp.route("/kpi/department-charters", methods=["GET"])
def department_charters():
    try:
        return jsonify(kpi_view.get_department_charters()), 200
    except Exception:
        logger.exception("Failed to fetch department charters")
        return jsonify({"error":"failed"}), 500

@bp.route("/kpi/returning-users", methods=["GET"])
def returning_users():
    days_raw = request.args.get("days", "15")
    try:
        days = int(days_raw)
    except Exception:
        days = 15
    try:
        data = kpi_view.get_returning_users(days=days)
        return jsonify(data), 200
    except Exception:
        logger.exception("Failed to fetch returning users")
        return jsonify({"error":"failed"}), 500

@bp.route("/kpi/user-activity", methods=["GET"])
def user_activity():
    limit_raw = request.args.get("limit", "10")
    try:
        limit = int(limit_raw)
    except Exception:
        limit = 10
    try:
        data = kpi_view.get_user_activity(limit=limit)
        return jsonify(data), 200
    except Exception:
        logger.exception("Failed to fetch user activity")
        return jsonify({"error":"failed"}), 500
