from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.services import get_user_decks, get_deck
from app.services.quiz_service import generate_quiz_data

bp = Blueprint('quiz', __name__, url_prefix='/quiz')

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
            'can_play': count >= 4
        })
    
    return render_template('quiz_dashboard.html', decks=playable_decks)

@bp.route('/<int:deck_id>')
@login_required
def start(deck_id):
    try:
        quiz_data = generate_quiz_data(current_user, deck_id)
        deck = get_deck(current_user, deck_id)
        
    except ValueError:
        flash("Ошибка при создании теста", "warning")
        return redirect(url_for('quiz.dashboard'))
        
    return render_template('quiz_run.html', deck=deck, questions=quiz_data)
