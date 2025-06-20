from werkzeug.security import generate_password_hash
from website.models import User, Note
from website import db


def signup(client, email='user@example.com', password='password', first='User'):
    return client.post('/signup', data={
        'email': email,
        'firstName': first,
        'password1': password,
        'password2': password,
    }, follow_redirects=False)


def login(client, email='user@example.com', password='password'):
    return client.post('/login', data={
        'email': email,
        'password': password,
    }, follow_redirects=False)


def test_signup_creates_user(client, app):
    resp = signup(client)
    assert resp.status_code in (302, 200)
    with app.app_context():
        assert User.query.filter_by(email='user@example.com').first() is not None
    with client.session_transaction() as sess:
        assert sess.get('_user_id') is not None


def test_login_and_logout(client, app):
    with app.app_context():
        user = User(email='login@example.com', firstName='Test',
                    password=generate_password_hash('secret'))
        db.session.add(user)
        db.session.commit()
        user_id = str(user.id)

    resp = login(client, 'login@example.com', 'secret')
    assert resp.status_code == 302
    with client.session_transaction() as sess:
        assert sess.get('_user_id') == user_id

    resp = client.get('/logout')
    assert resp.status_code == 302
    with client.session_transaction() as sess:
        assert '_user_id' not in sess


def test_note_crud(client, app):
    signup(client)
    resp = client.post('/', data={'note': 'my note'})
    assert resp.status_code == 200
    with app.app_context():
        user = User.query.filter_by(email='user@example.com').first()
        note = Note.query.filter_by(user_id=user.id).first()
        assert note and note.data == 'my note'
        note_id = note.id

    resp = client.post('/delete-note', json={'noteId': note_id})
    assert resp.status_code == 200
    with app.app_context():
        assert Note.query.get(note_id) is None
