import random
from app.services import get_deck_cards

def generate_quiz_data(user, deck_id, limit=20):
    cards = get_deck_cards(deck_id)
    
    if not cards:
        raise ValueError("Колода пуста")
        
    if cards[0].deck.user_id != user.id:
        raise ValueError("Нет доступа")

    if len(cards) < 4:
        raise ValueError("В колоде должно быть минимум 4 карточки для режима теста")

    questions_pool = list(cards)
    random.shuffle(questions_pool)
    selected_questions = questions_pool[:limit]

    quiz_data = []

    for card in selected_questions:
        correct = card.back
        other_cards = [c for c in cards if c.id != card.id]
        
        distractors = random.sample(other_cards, 3)
        distractors_text = [d.back for d in distractors]
        
        options = distractors_text + [correct]
        random.shuffle(options)
        
        quiz_data.append({
            'id': card.id,
            'question': card.front,
            'correct_answer': correct,
            'options': options
        })

    return quiz_data
