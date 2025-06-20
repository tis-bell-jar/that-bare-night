from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required,current_user
from .models import Note
from . import db
import json



views = Blueprint('views',__name__)

@views.route('/',methods=['GET','POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        color = request.form.get('color', '#ffff00')
        subject = request.form.get('subject', 'General')
        if len(note)<1:
            flash('Note is too short',category='error')
        else:
            # determine next position for the user's notes
            max_pos = db.session.query(db.func.max(Note.position)).filter_by(user_id=current_user.id).scalar()
            next_pos = (max_pos or 0) + 1
            new_note = Note(data=note, user_id=current_user.id,
                            position=next_pos, color=color, subject=subject)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added',category='success')

    notes = (Note.query.filter_by(user_id=current_user.id)
                     .order_by(Note.subject, Note.position).all())
    return render_template("home.html",user=current_user, notes=notes)

@views.route('/delete-note', methods=['POST'])
def delete_note():
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

