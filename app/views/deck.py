from flask import Blueprint, request, render_template, redirect, url_for, flash
from app.services import create_deck, get_deck, get_user_decks, delete_deck
from app.services import create_card, get_card, get_deck_cards, update_card, delete_card
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

@bp.route('/<int:deck_id>/delete', methods=['POST'])
@login_required
def delete(deck_id):
    try:
        delete_deck(current_user, deck_id)
        flash('Колода успешно удалена!', 'success')
    except ValueError:
        flash('Ошибка удаления колоды!', 'danger')
        
    return redirect(url_for('deck.index'))

@bp.route('/<int:deck_id>', methods=['GET', 'POST'])
@login_required
def details(deck_id):
    try:
        deck = get_deck(current_user, deck_id)
    except ValueError:
        flash("Колода не найдена", "danger")
        return redirect(url_for('deck.index'))

    form = CardForm()
    
    if form.validate_on_submit():
        try:
            create_card(current_user, deck.id, form.front.data, form.back.data)
            flash("Карточка добавлена!", "success")
            return redirect(url_for('deck.details', deck_id=deck.id))
        except ValueError:
            flash("Ошибка добавления карточки", "danger")

    cards = get_deck_cards(deck.id)
    return render_template('deck_details.html', deck=deck, cards=cards, form=form)

@bp.route('/card/<int:card_id>/delete', methods=['POST'])
@login_required
def remove_card(card_id):
    try:
        card = get_card(card_id) 
        deck_id = card.deck_id 
        delete_card(current_user, card_id)
        flash("Карточка удалена", "success")
        return redirect(url_for('deck.details', deck_id=deck_id))
    except ValueError:
        flash("Ошибка удаления", "danger")
        return redirect(url_for('deck.index'))

@bp.route('/card/<int:card_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_card(card_id):
    try:
        card = get_card(card_id)
    except ValueError:
        flash("Карточка не найдена", "danger")
        return redirect(url_for('deck.index'))

    form = CardForm()

    if request.method == 'GET':
        form.front.data = card.front
        form.back.data = card.back

    if form.validate_on_submit():
        try:
            update_card(current_user, card_id, new_front=form.front.data, new_back=form.back.data)
            flash("Карточка обновлена", "success")
            return redirect(url_for('deck.details', deck_id=card.deck_id))
        except ValueError:
            flash("Ошибка обновления карточки", "danger")

    return render_template('card_edit.html', form=form, card=card)
