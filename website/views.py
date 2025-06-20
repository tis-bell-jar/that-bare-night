from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
import json

from .models import Note
from . import db


views = Blueprint("views", __name__)


@views.route("/", methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        note_text = request.form.get("note")
        if not note_text:
            flash("Note is too short", category="error")
        else:
            new_note = Note(data=note_text, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note added", category="success")

    return render_template("home.html", user=current_user)


@views.route("/delete-note", methods=["POST"])
@login_required
def delete_note():
    note_data = json.loads(request.data)
    note = Note.query.get(note_data.get("noteId"))
    if note and note.user_id == current_user.id:
        db.session.delete(note)
        db.session.commit()
    return jsonify({})

