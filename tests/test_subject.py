import pytest
from website import create_app, db
from website.models import Note

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SECRET_KEY": "test-secret",
    })
    with app.app_context():
        db.create_all()
        yield app

@pytest.fixture
def client(app):
    return app.test_client()


def signup(client, email="user@example.com", password="password"):
    return client.post(
        "/signup",
        data={
            "email": email,
            "firstName": "Test",
            "password1": password,
            "password2": password,
        },
        follow_redirects=True,
    )


def login(client, email="user@example.com", password="password"):
    return client.post(
        "/login",
        data={"email": email, "password": password},
        follow_redirects=True,
    )


def test_note_subject_saved(client, app):
    signup(client)
    login(client)
    client.post(
        "/",
        data={"note": "test note", "subject": "math", "color": "#ff0000"},
        follow_redirects=True,
    )
    with app.app_context():
        note = Note.query.first()
        assert note.subject == "math"
