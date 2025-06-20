from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required,current_user
from .models import Note, Category
from . import db
import json



views = Blueprint('views',__name__)

@views.route('/',methods=['GET','POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        category_id = request.form.get('category_select')
        new_category_name = request.form.get('category_new')
        category = None
        if new_category_name:
            category = Category(name=new_category_name, user_id=current_user.id)
            db.session.add(category)
            db.session.commit()
        elif category_id:
            category = Category.query.filter_by(id=category_id, user_id=current_user.id).first()

        if len(note)<1:
            flash('Note is too short',category='error')
        else:
            new_note = Note(data=note,user_id=current_user.id, category_id=category.id if category else None)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added',category='success')

    categories = Category.query.filter_by(user_id=current_user.id).all()
    notes = current_user.notes
    return render_template("home.html",user=current_user, categories=categories, notes=notes)


@views.route('/category/<int:category_id>')
@login_required
def notes_by_category(category_id):
    category = Category.query.filter_by(id=category_id, user_id=current_user.id).first_or_404()
    categories = Category.query.filter_by(user_id=current_user.id).all()
    notes = Note.query.filter_by(user_id=current_user.id, category_id=category_id).all()
    return render_template("home.html", user=current_user, categories=categories, notes=notes, selected_category=category)

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

