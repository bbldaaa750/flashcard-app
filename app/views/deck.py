from flask import Blueprint, request, render_template, redirect, url_for, flash
from app.services import create_deck, get_deck, get_user_decks, update_deck, delete_deck
from flask_login import login_required, current_user

bp = Blueprint('deck', __name__, url_prefix='/deck')

@bp.route('/', methods=['GET', 'POST']) 
@login_required 
def index():
    if request.method == 'POST':
        title = request.form.get('title') 
        if title:
            try:
                create_deck(current_user, title)
                flash(f'Колода "{title}" создана!', 'success')
            except ValueError:
                flash('Колода уже существует!', 'error')
        else:
            flash('Название не может быть пустым', 'error')
        
        return redirect(url_for('deck.index'))

    user_decks = get_user_decks(current_user)
    return render_template('deck.html', decks=user_decks)

@bp.route('/<int:deck_id>/delete', methods=['POST'])
@login_required
def delete(deck_id):
    try:
        delete_deck(deck_id, current_user)
        flash('Колода успешно удалена!', 'success')
    except ValueError:
        flash('Ошибка удаления колоды!', 'error')
        
    return redirect(url_for('deck.index'))
