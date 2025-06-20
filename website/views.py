from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required,current_user
from .models import Note
from . import db
import json



views = Blueprint('views',__name__)


    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


@views.route('/reorder-notes', methods=['POST'])
@login_required
def reorder_notes():
    data = request.get_json()
    order = data.get('order', []) if data else []
    for position, note_id in enumerate(order):
        note = Note.query.get(int(note_id))
        if note and note.user_id == current_user.id:
            note.position = position + 1
    db.session.commit()
    return jsonify({'success': True})

