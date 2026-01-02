from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..services import entries_service

web_bp = Blueprint("web", __name__)


@web_bp.route("/")
def index():
    entries = entries_service.list_entries()
    return render_template("index.html", entries=entries)


@web_bp.route("/entries", methods=["POST"])
def create_entry():
    duration = request.form.get("duration_minutes", type=int)
    notes = request.form.get("notes")
    try:
        entries_service.create_entry(duration_minutes=duration, notes=notes)
        flash("Entry added", "success")
    except entries_service.ValidationError as exc:
        flash(str(exc), "error")
    return redirect(url_for("web.index"))


@web_bp.route("/entries/<int:entry_id>/delete", methods=["POST"])
def delete_entry(entry_id: int):
    entries_service.delete_entry(entry_id)
    flash("Entry deleted", "success")
    return redirect(url_for("web.index"))
