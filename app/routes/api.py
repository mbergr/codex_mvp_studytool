from flask import Blueprint, jsonify, request
from werkzeug.exceptions import BadRequest
from ..services import entries_service

api_bp = Blueprint("api", __name__)


def _parse_json():
    if not request.is_json:
        raise BadRequest("Expected JSON body")
    return request.get_json() or {}


@api_bp.route("/entries", methods=["GET"])
def list_entries():
    entries = entries_service.list_entries()
    return jsonify([entry.to_dict() for entry in entries])


@api_bp.route("/entries", methods=["POST"])
def create_entry():
    data = _parse_json()
    duration = data.get("duration_minutes")
    notes = data.get("notes")
    practiced_at = data.get("practiced_at")
    try:
        entry = entries_service.create_entry(
            duration_minutes=duration,
            notes=notes,
            practiced_at=practiced_at,
        )
    except entries_service.ValidationError as exc:
        raise BadRequest(str(exc)) from exc
    return jsonify(entry.to_dict()), 201


@api_bp.route("/entries/<int:entry_id>", methods=["DELETE"])
def delete_entry(entry_id: int):
    entries_service.delete_entry(entry_id)
    return "", 204
