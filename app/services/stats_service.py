from sqlalchemy import func
from app.extensions import db
from app.models import Card, Deck

def get_user_statistics(user):
    decks_data = {}
    for deck in user.decks:
        decks_data[deck.id] = {
            'title': deck.title,
            'box1': 0, 'box2': 0, 'box3': 0,
            'total': 0
        }

    query = db.session.query(
        Card.deck_id,
        Card.box,
        func.count(Card.id)
    ).join(Deck).filter(Deck.user_id == user.id).group_by(Card.deck_id, Card.box).all()

    for deck_id, box, count in query:
        if deck_id in decks_data:
            if box >= 3:
                key = 'box3'
            elif box == 2:
                key = 'box2'
            else:
                key = 'box1'
            
            decks_data[deck_id][key] += count
            decks_data[deck_id]['total'] += count

    total_stats = {'box1': 0, 'box2': 0, 'box3': 0, 'total': 0}
    for d in decks_data.values():
        total_stats['box1'] += d['box1']
        total_stats['box2'] += d['box2']
        total_stats['box3'] += d['box3']
        total_stats['total'] += d['total']
        
    return {
        'total': total_stats,
        'decks': decks_data
    }
