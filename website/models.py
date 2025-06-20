from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from enum import Enum
from markdown import markdown
import bleach


class Color(Enum):
    """Available note colors."""
    RED = "red"
    GREEN = "green"
    BLUE = "blue"
    YELLOW = "yellow"


class Position(Enum):
    """Possible CSS position classes for notes."""
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"

class Note(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True),default=func.now())
    position = db.Column(db.Integer, default=0)
    color = db.Column(db.String(20), default=Color.YELLOW.value)
    position_class = db.Column(db.String(20), default=Position.LEFT.value)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    ALLOWED_TAGS = bleach.sanitizer.ALLOWED_TAGS + [
        "p",
        "pre",
        "span",
    ]
    ALLOWED_ATTRIBUTES = {"span": ["class"], "a": ["href", "title"]}

    @property
    def html(self) -> str:
        """Return sanitized HTML representation of the note."""
        raw_html = markdown(self.data or "", output_format="html")
        return bleach.clean(raw_html, tags=self.ALLOWED_TAGS, attributes=self.ALLOWED_ATTRIBUTES)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(150),unique=True)
    password = db.Column(db.String(150))
    firstName = db.Column(db.String(150))
    notes = db.relationship('Note')

