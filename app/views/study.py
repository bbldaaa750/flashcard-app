import random
from flask import Blueprint, render_template, redirect, url_for, flash, jsonify, request
from flask_login import login_required, current_user
from app.services import get_deck, get_deck_cards
from app.services import get_cards_due_today, process_review

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

@bp.route('/leitner')
@login_required
def leitner_index():
    deck_id = request.args.get('deck_id', type=int)
    
    cards_objects = get_cards_due_today(current_user, deck_id)
    
    if not cards_objects:
        flash("На сегодня всё выучено! Возвращайтесь завтра.", "success")
        return redirect(url_for('deck.index'))

    cards_data = [
        {'id': c.id, 'front': c.front, 'back': c.back, 'box': c.box} 
        for c in cards_objects
    ]
    
    random.shuffle(cards_data)
    return render_template('leitner_study.html', cards_json=cards_data)


@bp.route('/review/<int:card_id>', methods=['POST'])
@login_required
def save_review(card_id):
    data = request.get_json()
    rating = data.get('rating')
    
    if rating not in ['fail', 'hard', 'good']:
        return jsonify({'error': 'Ошибка рейтинга'}), 400
        
    try:
        result = process_review(current_user, card_id, rating)
        return jsonify({'status': 'ok', 'result': result})
    except ValueError:
        return jsonify({'error': 'Доступ запрещён'}), 403
