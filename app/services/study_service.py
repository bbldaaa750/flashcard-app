from datetime import date, timedelta
from app.extensions import db
from app.models import Card
from app.services.card_service import get_card

BOX_INTERVALS = {
    1: 1,
    2: 3,
    3: 5,
}

def get_cards_due_today(user, deck_id=None):
    query = Card.query.join(Card.deck).filter(
        Card.deck.user_id == user.id,
        Card.next_review_date <= date.today()
    )
    
    if deck_id:
        query = query.filter(Card.deck_id == deck_id)
        
    return query.all()


def process_review(user, card_id, rating):
    card = get_card(card_id)
    
    if card.deck.user_id != user.id:
        raise ValueError("Access denied")

    if rating == 'fail':
        card.box -= 1
        if card.box < 1: 
            card.box = 1
        interval = 1
    elif rating == 'hard':
        interval = 1
    elif rating == 'good':
        card.box += 1
        if card.box > 3:
            card.box = 3
        interval = BOX_INTERVALS[card.box]

    card.next_review_date = date.today() + timedelta(days=interval)
    
    db.session.commit()
    
    return {
        'new_box': card.box,
        'next_review': card.next_review_date.strftime('%Y-%m-%d')
    }
