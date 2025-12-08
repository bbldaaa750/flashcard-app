import random
import json
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.services import get_deck, get_deck_cards

bp = Blueprint('study', __name__, url_prefix='/study')

@bp.route('/<int:deck_id>')
@login_required
def start(deck_id):
    try:
        deck = get_deck(current_user, deck_id)
    except ValueError:
        flash("Колода не найдена", "danger")
        return redirect(url_for('deck.index'))

    cards_objects = get_deck_cards(deck.id)
    
    if not cards_objects:
        flash("В этой колоде нет карточек для изучения", "warning")
        return redirect(url_for('deck.details', deck_id=deck.id))

    cards_data = [
        {'id': c.id, 'front': c.front, 'back': c.back} 
        for c in cards_objects
    ]
    
    random.shuffle(cards_data)
    return render_template('study.html', deck=deck, cards_json=cards_data)
