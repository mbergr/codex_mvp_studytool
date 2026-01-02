from datetime import datetime
from sqlalchemy import DateTime, Integer, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from .db import db


class PracticeEntry(db.Model):
    __tablename__ = "practice_entries"
    __table_args__ = (
        db.Index("ix_practice_entries_practiced_at", "practiced_at"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    practiced_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "practiced_at": self.practiced_at.isoformat() if self.practiced_at else None,
            "duration_minutes": self.duration_minutes,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
