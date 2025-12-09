let currentIndex = 0;
let score = 0;

const contentDiv = document.getElementById('quiz-content');
const questionText = document.getElementById('question-text');
const answerInput = document.getElementById('answer-input');
const checkBtn = document.getElementById('check-btn');
const feedbackArea = document.getElementById('feedback-area');
const feedbackTitle = document.getElementById('feedback-title');
const correctAnswerDisplay = document.getElementById('correct-answer-display');
const footerNav = document.getElementById('footer-nav');
const nextBtn = document.getElementById('next-btn');
const counter = document.getElementById('counter');
const total = document.getElementById('total');

total.innerText = cards.length;

function renderCard() {
    if (currentIndex >= cards.length) {
        showResults();
        return;
    }

    const card = cards[currentIndex];
    
    questionText.innerText = card.front;
    counter.innerText = currentIndex + 1;
    
    answerInput.value = '';
    answerInput.disabled = false;
    answerInput.classList.remove('is-valid', 'is-invalid');
    answerInput.focus();
    
    feedbackArea.classList.add('d-none');
    footerNav.classList.add('d-none');
    checkBtn.classList.remove('d-none');
}

function checkAnswer() {
    const card = cards[currentIndex];
    const userAnswer = answerInput.value.trim().toLowerCase();
    const correctAnswer = card.back.trim().toLowerCase();
    
    if (!userAnswer) return;

    answerInput.disabled = true;
    checkBtn.classList.add('d-none');

    if (userAnswer === correctAnswer) {
        score++;
        answerInput.classList.add('is-valid');
        feedbackTitle.innerText = "Правильно! 🎉";
        feedbackTitle.className = "fw-bold mb-2 text-success";
        correctAnswerDisplay.innerText = "";
    } else {
        answerInput.classList.add('is-invalid');
        feedbackTitle.innerText = "Ошибка 😞";
        feedbackTitle.className = "fw-bold mb-2 text-danger";
        correctAnswerDisplay.innerHTML = `Правильный ответ: <span class="fw-bold text-dark">${card.back}</span>`;
    }

    feedbackArea.classList.remove('d-none');
    footerNav.classList.remove('d-none');
    
    nextBtn.focus();
}

function showResults() {
    contentDiv.innerHTML = `
        <div class="text-center mt-5">
            <h1 class="display-4 mb-4">Результат: ${score} / ${cards.length}</h1>
            <p class="lead text-muted">Отличная тренировка правописания!</p>
            <a href="/typing/dashboard" class="btn btn-primary btn-lg mt-4">К списку тестов</a>
        </div>
    `;
    footerNav.classList.add('d-none');
}

checkBtn.addEventListener('click', checkAnswer);

answerInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        checkAnswer();
    }
});

nextBtn.addEventListener('click', function() {
    currentIndex++;
    renderCard();
});

renderCard();
