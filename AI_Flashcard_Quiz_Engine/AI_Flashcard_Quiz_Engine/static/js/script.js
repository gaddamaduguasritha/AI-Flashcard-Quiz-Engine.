document.addEventListener("DOMContentLoaded", function () {
  const generateForm = document.getElementById("generateForm");
  if (generateForm) {
    generateForm.addEventListener("submit", function () {
      const indicator = document.getElementById("loadingIndicator");
      const button = document.getElementById("generateButton");
      if (indicator) indicator.classList.remove("d-none");
      if (button) {
        button.disabled = true;
        button.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Generating...';
      }
    });
  }

  const flashcard = document.getElementById("flashcard");
  if (flashcard) {
    const dataElement = document.getElementById("flashcardData");
    const parts = dataElement.textContent.split("__SPLIT__");
    let fronts = [];
    let backs = [];
    try {
      fronts = JSON.parse(parts[0]);
      backs = JSON.parse(parts[1]);
    } catch (error) {
      fronts = [];
      backs = [];
    }

    let order = fronts.map((_, index) => index);
    let current = 0;

    const frontElement = document.getElementById("cardFront");
    const backElement = document.getElementById("cardBack");
    const counter = document.getElementById("cardCounter");
    const totalElement = document.getElementById("cardTotal");

    function renderCard() {
      if (!fronts.length) return;
      const index = order[current];
      frontElement.textContent = fronts[index];
      backElement.textContent = backs[index];
      counter.textContent = current + 1;
      totalElement.textContent = fronts.length;
      flashcard.classList.remove("flipped");
    }

    flashcard.addEventListener("click", function () {
      flashcard.classList.toggle("flipped");
    });

    document.getElementById("flipCard").addEventListener("click", function () {
      flashcard.classList.toggle("flipped");
    });

    document.getElementById("nextCard").addEventListener("click", function () {
      current = (current + 1) % order.length;
      renderCard();
    });

    document.getElementById("prevCard").addEventListener("click", function () {
      current = (current - 1 + order.length) % order.length;
      renderCard();
    });

    document.getElementById("shuffleCards").addEventListener("click", function () {
      for (let i = order.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [order[i], order[j]] = [order[j], order[i]];
      }
      current = 0;
      renderCard();
    });

    document.getElementById("regenerateCards").addEventListener("click", function () {
      document.getElementById("regeneratePanel").classList.toggle("d-none");
    });

    renderCard();
  }

  const quizForm = document.getElementById("quizForm");
  if (quizForm) {
    const questions = document.querySelectorAll(".quiz-question");
    const progressBar = document.getElementById("quizProgress");

    function updateProgress() {
      let answered = 0;
      questions.forEach(function (card) {
        if (card.querySelector("input[type=radio]:checked")) answered++;
      });
      const percent = questions.length ? (answered / questions.length) * 100 : 0;
      progressBar.style.width = percent + "%";
    }

    quizForm.addEventListener("change", function (event) {
      if (event.target.type === "radio") {
        const card = event.target.closest(".quiz-question");
        card.querySelectorAll(".quiz-option").forEach(function (option) {
          option.classList.remove("selected");
        });
        event.target.closest(".quiz-option").classList.add("selected");
        updateProgress();
      }
    });

    updateProgress();
  }
});
