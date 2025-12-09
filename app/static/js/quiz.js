let currentIndex = 0;
let score = 0;

const questionText = document.getElementById('question-text');
const optionsContainer = document.getElementById('options-container');
const counter = document.getElementById('counter');
const total = document.getElementById('total');
const nextBtn = document.getElementById('next-btn');
const footerNav = document.getElementById('footer-nav');

total.innerText = questions.length;

function renderQuestion() {
    if (currentIndex >= questions.length) {
        showResults();
        return;
    }

    const q = questions[currentIndex];
    
    questionText.innerText = q.question;
    counter.innerText = currentIndex + 1;
    footerNav.classList.add('d-none'); 
    
    optionsContainer.innerHTML = '';

    q.options.forEach(optionText => {
        const btn = document.createElement('button');
        btn.className = 'btn btn-outline-dark p-3 text-start fs-5';
        btn.innerText = optionText;
        
        btn.onclick = () => checkAnswer(btn, optionText, q.correct_answer);
        
        optionsContainer.appendChild(btn);
    });
}

function checkAnswer(selectedBtn, selectedText, correctText) {
    const allBtns = optionsContainer.querySelectorAll('button');
    allBtns.forEach(btn => btn.disabled = true);

    if (selectedText === correctText) {
        selectedBtn.classList.remove('btn-outline-dark');
        selectedBtn.classList.add('btn-success');
        score++;
    } else {
        selectedBtn.classList.remove('btn-outline-dark');
        selectedBtn.classList.add('btn-danger');
        
        allBtns.forEach(btn => {
            if (btn.innerText === correctText) {
                btn.classList.remove('btn-outline-dark');
                btn.classList.add('btn-success');
            }
        });
    }

    footerNav.classList.remove('d-none');
}

function showResults() {
    questionText.innerText = `Тест завершен! 🎉`;
    optionsContainer.innerHTML = `
        <div class="text-center">
            <h3>Ваш результат: ${score} из ${questions.length}</h3>
            <p class="text-muted mt-3">Отличная работа!</p>
            <a href="/quiz/dashboard" class="btn btn-primary mt-3">К списку тестов</a>
        </div>
    `;
    footerNav.classList.add('d-none');
}

nextBtn.onclick = () => {
    currentIndex++;
    renderQuestion();
};

renderQuestion();
