from __future__ import annotations
from datetime import datetime
from typing import Iterable
from flask import abort
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..db import db
from ..models import PracticeEntry


class ValidationError(ValueError):
    pass


def _validate_duration(duration_minutes: int | None) -> int:
    if duration_minutes is None:
        raise ValidationError("Duration is required")
    if duration_minutes <= 0:
        raise ValidationError("Duration must be greater than 0")
    return duration_minutes


def _validate_practiced_at(practiced_at: datetime | str | None) -> datetime:
    if practiced_at is None:
        return datetime.now().astimezone()
    if isinstance(practiced_at, str):
        try:
            practiced_at = datetime.fromisoformat(practiced_at)
        except ValueError as exc:
            raise ValidationError("Invalid practiced_at format") from exc
    if practiced_at.tzinfo is None:
        practiced_at = practiced_at.astimezone()
    return practiced_at


def _validate_notes(notes: str | None) -> str | None:
    if notes:
        return notes.strip()
    return None


def create_entry(
    *, duration_minutes: int | None, notes: str | None = None, practiced_at: datetime | str | None = None
) -> PracticeEntry:
    duration = _validate_duration(duration_minutes)
    practice_time = _validate_practiced_at(practiced_at)
    clean_notes = _validate_notes(notes)

    entry = PracticeEntry(
        duration_minutes=duration, practiced_at=practice_time, notes=clean_notes
    )

    session: Session = db.session
    session.add(entry)
    session.commit()
    session.refresh(entry)
    return entry


def list_entries(limit: int = 20) -> Iterable[PracticeEntry]:
    session: Session = db.session
    stmt = (
        select(PracticeEntry)
        .order_by(PracticeEntry.practiced_at.desc(), PracticeEntry.id.desc())
        .limit(limit)
    )
    return session.scalars(stmt).all()


def delete_entry(entry_id: int) -> None:
    session: Session = db.session
    entry = session.get(PracticeEntry, entry_id)
    if not entry:
        abort(404, description="Entry not found")
    session.delete(entry)
    session.commit()
