from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import markdown
import bleach


ALLOWED_TAGS = bleach.sanitizer.ALLOWED_TAGS + [
    "p",
    "pre",
    "code",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
]
ALLOWED_ATTRIBUTES = {**bleach.sanitizer.ALLOWED_ATTRIBUTES, "img": ["src", "alt"]}

class Note(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True),default=func.now())
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    def to_html(self) -> str:
        """Return sanitized HTML representation of the note's Markdown."""
        raw_html = markdown.markdown(self.data or "")
        clean_html = bleach.clean(
            raw_html,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=True,
        )
        return clean_html


class User(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(150),unique=True)
    password = db.Column(db.String(150))
    firstName = db.Column(db.String(150))
    notes = db.relationship('Note')

