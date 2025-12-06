from flask import Blueprint, request, render_template, redirect, url_for, flash
from app.services import create_deck, get_deck, get_user_decks, update_deck, delete_deck
from flask_login import login_required, current_user

bp = Blueprint('decks', __name__, url_prefix='/decks')

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
        
        return redirect(url_for('decks.index'))

    user_decks = get_user_decks(current_user)
    return render_template('decks/index.html', decks=user_decks)


@bp.route('/<int:deck_id>/delete', methods=['POST'])
@login_required
def delete(deck_id):
    try:
        delete_deck(deck_id, current_user)
        flash('Колода удалена', 'success')
    except ValueError:
        flash('Ошибка удаления', 'error')
        
    return redirect(url_for('decks.index'))
