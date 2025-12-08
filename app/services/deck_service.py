from app.models import Deck
from app.extensions import db

def create_deck(user, title):
    if Deck.query.filter_by(title=title, user_id=user.id).first():
        raise ValueError(f'Deck "{title}" already exists for this user')
    deck = Deck(title=title, user_id=user.id)
    db.session.add(deck)
    db.session.commit()
    return deck

def get_deck(user, deck_id):
    deck = Deck.query.get(deck_id)
    if not deck:
        raise ValueError(f'Deck with id {deck_id} not found')
    if deck.user_id != user.id:
        raise ValueError('Access denied: not your deck')
    return deck

def get_user_decks(user):
    return user.decks

def update_deck(user, deck_id, new_title=None):
    deck = get_deck(user, deck_id)
    if new_title and Deck.query.filter_by(title=new_title, user_id=user.id).first():
        raise ValueError(f'Deck "{new_title}" already exists for this user')
    if new_title:
        deck.title = new_title
    db.session.commit()
    return deck

def delete_deck(user, deck_id):
    deck = get_deck(user, deck_id)
    db.session.delete(deck)
    db.session.commit()
    return True
