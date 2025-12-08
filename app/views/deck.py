from flask import Blueprint, render_template, redirect, url_for, flash
from app.services import create_deck, get_deck, get_user_decks, delete_deck, create_card, get_deck_cards
from flask_login import login_required, current_user
from app.forms import DeckForm, CardForm

bp = Blueprint('deck', __name__, url_prefix='/deck')

@bp.route('/', methods=['GET', 'POST']) 
@login_required 
def index():
    form = DeckForm()
    if form.validate_on_submit():
        title = form.title.data 
        try:
            create_deck(current_user, title)
            flash(f'Колода "{title}" создана!', 'success')
            return redirect(url_for('deck.index'))
        except ValueError:
            flash('Колода уже существует!', 'danger')
            
    user_decks = get_user_decks(current_user)
    return render_template('deck.html', decks=user_decks, form=form)

@bp.route('/<int:deck_id>', methods=['GET', 'POST'])
@login_required
def details(deck_id):
    try:
        deck = get_deck(deck_id, current_user)
    except ValueError:
        flash("Колода не найдена или доступ запрещен", "danger")
        return redirect(url_for('deck.index'))

    form = CardForm()
    if form.validate_on_submit():
        try:
            create_card(deck.id, form.front.data, form.back.data)
            flash("Карточка добавлена!", "success")
            return redirect(url_for('deck.details', deck_id=deck.id))
        except ValueError as e:
            flash(str(e), "danger")

    cards = get_deck_cards(deck.id)
    return render_template('deck_details.html', deck=deck, cards=cards, form=form)

@bp.route('/<int:deck_id>/delete', methods=['POST'])
@login_required
def delete(deck_id):
    try:
        delete_deck(deck_id, current_user)
        flash('Колода успешно удалена!', 'success')
    except ValueError:
        flash('Ошибка удаления колоды!', 'danger')
        
    return redirect(url_for('deck.index'))
