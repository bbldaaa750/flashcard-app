from app.models import Card, Deck
from app.extensions import db

def create_card(deck_id, front, back):
    if not Deck.query.get(deck_id):
        raise ValueError(f'Deck with id {deck_id} not found')

    if Card.query.filter_by(deck_id=deck_id, front=front).first():
        raise ValueError(f'Card with question "{front}" already exists in this deck')

    card = Card(deck_id=deck_id, front=front, back=back)
    db.session.add(card)
    db.session.commit()
    return card

def get_card(card_id):
    card = Card.query.get(card_id)
    if not card:
        raise ValueError(f'Card with id {card_id} not found')
    return card

def get_deck_cards(deck_id):
    deck = Deck.query.get(deck_id)
    if not deck:
        raise ValueError(f'Deck {deck_id} not found')
    return deck.cards 

def update_card(card_id, new_front=None, new_back=None):
    card = get_card(card_id)

    if new_front and new_front != card.front:
        existing = Card.query.filter_by(deck_id=card.deck_id, front=new_front).first()
        if existing:
            raise ValueError(f'Card "{new_front}" already exists')
        card.front = new_front

    if new_back:
        card.back = new_back
        
    db.session.commit()
    return card

def delete_card(card_id):
    card = get_card(card_id)
    db.session.delete(card)
    db.session.commit()
    return True
