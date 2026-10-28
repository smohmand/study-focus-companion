/*
File: script.js
Project: Study & Focus Companion
Description: Handles backend API calls and Pomodoro timer countdown logic.
Author: Milan Bennett
Date: October 2026
*/

// pomodoro logic
let timeLeft = 25 * 60; // 25 minutes in seconds
let timerId = null;

const timerDisplay = document.getElementById('timerDisplay');
const startBtn = document.getElementById('startBtn');
const pauseBtn = document.getElementById('pauseBtn');
const resetBtn = document.getElementById('resetBtn');

function updateDisplay() {
    const minutes = Math.floor(timeLeft / 60);
    const seconds = timeLeft % 60;
    timerDisplay.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
}

startBtn.addEventListener('click', () => {
    if (timerId !== null) return;
    timerId = setInterval(() => {
        if (timeLeft > 0) {
            timeLeft--;
            updateDisplay();
        } else {
            clearInterval(timerId);
            timerId = null;
            alert("Focus session complete! Time for a break.");
        }
    }, 1000);
});

pauseBtn.addEventListener('click', () => {
    clearInterval(timerId);
    timerId = null;
});

resetBtn.addEventListener('click', () => {
    clearInterval(timerId);
    timerId = null;
    timeLeft = 25 * 60;
    updateDisplay();
});

// initialize display
updateDisplay();

// api text processing
document.getElementById('processBtn').addEventListener('click', async () => {
    const textValue = document.getElementById('studyInput').value;
    const summaryElement = document.getElementById('summaryOutput');
    const flashcardElement = document.getElementById('flashcardOutput');

    if (!textValue.trim()) {
        alert('Please enter some study text first!');
        return;
    }

    summaryElement.textContent = 'Generating summary...';
    flashcardElement.textContent = 'Generating flashcards...';

    try {
        const response = await fetch('/process-text', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: textValue })
        });

        const data = await response.json();
        summaryElement.textContent = data.summary;

        flashcardElement.innerHTML = '';
        data.flashcards.forEach((card, index) => {
            const cardDiv = document.createElement('div');
            cardDiv.className = 'flashcard-item';
            cardDiv.innerHTML = `<strong>Q${index + 1}:</strong> ${card.question}<br><em>A:</em> ${card.answer}`;
            flashcardElement.appendChild(cardDiv);
        });
    } catch (error) {
        console.error('Error connecting to backend:', error);
        summaryElement.textContent = 'Failed to generate materials.';
    }
});