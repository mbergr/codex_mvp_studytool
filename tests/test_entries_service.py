import pytest
from app import create_app
from app.config import TestConfig
from app.db import db
from app.services import entries_service


@pytest.fixture()
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


def test_create_and_list_entries(app):
    with app.app_context():
        entries_service.create_entry(duration_minutes=20, notes="Scales")
        entries_service.create_entry(duration_minutes=10, notes=None)

        entries = entries_service.list_entries()
        assert len(entries) == 2
        assert entries[0].duration_minutes in {10, 20}


def test_create_entry_validation(app):
    with app.app_context():
        with pytest.raises(entries_service.ValidationError):
            entries_service.create_entry(duration_minutes=0)


def test_delete_entry(app):
    with app.app_context():
        entry = entries_service.create_entry(duration_minutes=15, notes="Chords")
        entries_service.delete_entry(entry.id)
        assert entries_service.list_entries() == []
