import random
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.services import get_user_decks, get_deck, get_deck_cards

bp = Blueprint('typing', __name__, url_prefix='/typing')

@bp.route('/dashboard')
@login_required
def dashboard():
    all_decks = get_user_decks(current_user)
    
    playable_decks = []
    for deck in all_decks:
        count = len(deck.cards)
        playable_decks.append({
            'deck': deck,
            'count': count,
            'can_play': count >= 1
        })
    
    return render_template('typing_dashboard.html', decks=playable_decks)

@bp.route('/<int:deck_id>')
@login_required
def start(deck_id):
    try:
        deck = get_deck(current_user, deck_id)
        cards_objects = get_deck_cards(deck.id)
        
        if not cards_objects:
            flash("Колода пуста", "warning")
            return redirect(url_for('typing.dashboard'))
            
        cards_data = [
            {'id': c.id, 'front': c.front, 'back': c.back} 
            for c in cards_objects
        ]
        random.shuffle(cards_data)
        
    except ValueError:
        flash("Ошибка при создании письменного ввода", "warning")
        return redirect(url_for('typing.dashboard'))
        
    return render_template('typing.html', deck=deck, cards=cards_data)
