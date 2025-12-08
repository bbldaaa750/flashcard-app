let currentIndex = 0;
let isFlipped = false;

const cardElement = document.getElementById('flashcard');
const frontText = document.getElementById('card-front-text');
const backText = document.getElementById('card-back-text');
const counter = document.getElementById('counter');
const nextBtn = document.getElementById('next-btn');
const prevBtn = document.getElementById('prev-btn');

function renderCard() {
    if (currentIndex >= cards.length) {
        if (isFlipped) {
            cardElement.style.transform = 'rotateY(0deg)';
            isFlipped = false;
        }

        frontText.innerText = "Всё выучено! 🎉";
        backText.innerText = "";
        cardElement.style.pointerEvents = "none";
        
        nextBtn.disabled = true;
        nextBtn.innerText = "Конец";
        prevBtn.disabled = false;
        
    } else {
        const card = cards[currentIndex];
        frontText.innerText = card.front;
        backText.innerText = card.back;
        counter.innerText = currentIndex + 1;
        
        cardElement.style.pointerEvents = "auto";
        nextBtn.disabled = false;
        nextBtn.innerText = "Далее \u2192";
        prevBtn.disabled = (currentIndex === 0);
    }
}

document.querySelector('.scene').addEventListener('click', function() {
    if (currentIndex >= cards.length) return;

    isFlipped = !isFlipped;
    if (isFlipped) {
        cardElement.style.transform = 'rotateY(180deg)';
    } else {
        cardElement.style.transform = 'rotateY(0deg)';
    }
});

nextBtn.addEventListener('click', function(e) {
    e.stopPropagation();

    if (currentIndex < cards.length) {
        if (isFlipped) {
            isFlipped = false;
            cardElement.style.transform = 'rotateY(0deg)';
            setTimeout(() => {
                currentIndex++;
                renderCard();
            }, 600);
        } else {
            currentIndex++;
            renderCard();
        }
    }
});

prevBtn.addEventListener('click', function(e) {
    e.stopPropagation();
    if (currentIndex > 0) {
        if (isFlipped) {
            cardElement.style.transform = 'rotateY(0deg)';
            isFlipped = false;
            setTimeout(() => {
                currentIndex--;
                renderCard();
            }, 600);
        } else {
            currentIndex--;
            renderCard();
        }
    }
});

renderCard();
