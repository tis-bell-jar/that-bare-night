from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from enum import Enum


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


class User(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(150),unique=True)
    password = db.Column(db.String(150))
    firstName = db.Column(db.String(150))
    notes = db.relationship('Note')

