let currentIndex = 0;
let isFlipped = false;

const cardElement = document.getElementById('flashcard');
const frontText = document.getElementById('card-front-text');
const backText = document.getElementById('card-back-text');
const counter = document.getElementById('counter');
const ratingButtonsContainer = document.getElementById('rating-buttons');
const flipHint = document.getElementById('flip-hint');

function renderCard() {
    if (currentIndex >= cards.length) {
        if (counter) counter.innerText = "0"
        frontText.innerText = "На сегодня всё! 🎉";
        backText.innerText = "";
        cardElement.style.pointerEvents = "none";
        ratingButtonsContainer.classList.add('invisible');
        flipHint.innerText = "Возвращайся завтра";
        return;
    }

    const card = cards[currentIndex];
    frontText.innerText = card.front;
    backText.innerText = card.back;
    
    counter.innerText = cards.length - currentIndex;

    isFlipped = false;
    cardElement.style.transform = 'rotateY(0deg)';
    ratingButtonsContainer.classList.add('invisible');
    flipHint.classList.remove('invisible');
}

cardElement.addEventListener('click', function() {
    if (currentIndex >= cards.length) return;
    
    if (!isFlipped) {
        isFlipped = true;
        cardElement.style.transform = 'rotateY(180deg)';
        
        ratingButtonsContainer.classList.remove('invisible');
        flipHint.classList.add('invisible');
    }
});

document.querySelectorAll('.rating-btn').forEach(button => {
    button.addEventListener('click', function() {
        const rating = this.dataset.rating;
        const currentCard = cards[currentIndex];

        sendReview(currentCard.id, rating);
        ratingButtonsContainer.classList.add('invisible');

        if (isFlipped) {
            cardElement.style.transform = 'rotateY(0deg)';
            isFlipped = false;
            setTimeout(() => {
                currentIndex++;
                renderCard();
            }, 600);
        } else {
            currentIndex++;
            renderCard();
        }
    });
});

function sendReview(cardId, rating) {
    const url = reviewBaseUrl + cardId;
    
    fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ rating: rating }) 
    })
    .then(response => {
        if (!response.ok) {
            console.error("Ошибка сохранения!", response);
        }
        return response.json();
    })
    .then(data => {
        console.log("Успех:", data);
    })
    .catch(error => {
        console.error("Ошибка сети:", error);
    });
}

renderCard();
