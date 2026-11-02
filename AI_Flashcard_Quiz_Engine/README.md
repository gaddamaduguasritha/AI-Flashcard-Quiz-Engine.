# AI Flashcard and Quiz Engine from Lecture Notes

A Flask web application that converts lecture notes into interactive flashcards, multiple-choice quizzes, true/false questions, scores, explanations, and revision material.

## Problem Statement

Students often have long lecture notes but limited time to revise. Manually creating flashcards and practice questions is slow and repetitive. This project automatically analyzes lecture notes and produces useful study material.

## Objectives

- Upload or paste lecture notes in TXT, PDF, or DOCX format.
- Extract and clean readable text.
- Generate flashcards from definitions, keywords, and important sentences.
- Generate MCQs and true/false questions related to the notes.
- Calculate quiz scores and provide answer explanations.
- Store notes, flashcards, quizzes, and attempts in SQLite.
- Work completely offline using local NLP, with optional AI API support.

## Technology Stack

- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5
- **Backend:** Python 3, Flask
- **Database:** SQLite
- **File parsing:** PyPDF2, python-docx
- **Local AI/NLP:** Rule-based sentence analysis, keyword frequency, definition detection, sentence ranking
- **Optional AI:** OpenAI-compatible chat completion API

## Project Structure

```text
AI_Flashcard_Quiz_Engine/
├── app.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── generate.html
│   ├── flashcards.html
│   ├── quiz.html
│   ├── results.html
│   ├── history.html
│   ├── note_details.html
│   ├── about.html
│   └── error.html
├── static/
│   ├── css/style.css
│   ├── js/script.js
│   └── images/
├── uploads/
├── database/
│   └── app.db
├── sample_data/
│   └── artificial_intelligence_notes.txt
├── utils/
│   ├── __init__.py
│   ├── database.py
│   ├── file_parser.py
│   ├── text_processor.py
│   ├── flashcard_generator.py
│   ├── quiz_generator.py
│   └── ai_client.py
└── docs/
    ├── PROJECT_REPORT.md
    ├── ABSTRACT.md
    ├── INSTALLATION.md
    ├── VIVA_QUESTIONS.md
    └── TEST_CASES.md
```

## Database Schema

| Table | Purpose | Important columns |
|---|---|---|
| `notes` | Stores lecture notes | `id`, `title`, `source_type`, `content`, `generator_mode`, `created_at` |
| `flashcards` | Stores generated flashcards | `id`, `note_id`, `front`, `back`, `position` |
| `quizzes` | Stores generated quizzes | `id`, `note_id`, `difficulty`, `generator_mode`, `created_at` |
| `quiz_questions` | Stores quiz questions | `id`, `quiz_id`, `question_type`, `question_text`, `options_json`, `correct_answer`, `explanation` |
| `quiz_attempts` | Stores student quiz attempts | `id`, `quiz_id`, `note_id`, `score`, `total`, `percentage`, `answers_json`, `created_at` |

The database file `database/app.db` is created automatically when the application starts.

## Installation on Windows

Open Command Prompt or PowerShell in the extracted project folder and run:

```bat
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## Usage

1. Open the home page and click **Get Started**.
2. Enter a title.
3. Paste lecture notes or upload a `.txt`, `.pdf`, or `.docx` file.
4. Select the number of flashcards, number of quiz questions, difficulty, and generation mode.
5. Click **Generate Study Material**.
6. Study the flashcards using flip, previous, next, shuffle, and regenerate controls.
7. Start the quiz, answer all questions, and submit.
8. View your score, percentage, correct answers, incorrect answers, and explanations.
9. Use **History** to revisit saved sessions and quiz attempts.
10. Download flashcards as TXT or JSON, download quiz results, or print results.

## Sample Data

A ready-made sample is included at:

```text
sample_data/artificial_intelligence_notes.txt
```

Open it, copy its contents into the notes box, and generate study material.

## AI/NLP Methodology

The offline engine uses:

1. **Text cleaning:** Removes extra whitespace and invalid control characters.
2. **Sentence tokenization:** Splits notes into meaningful sentences.
3. **Keyword extraction:** Filters stop words and ranks repeated academic terms.
4. **Definition detection:** Finds patterns such as “X is…”, “X refers to…”, and “X means…”.
5. **Sentence ranking:** Ranks sentences using keyword density, sentence length, and position.
6. **Flashcard generation:** Creates definition cards, fill-in-the-blank cards, and concept explanation cards.
7. **Quiz generation:** Creates definition MCQs, keyword-based cloze MCQs, and true/false questions.
8. **Distractor generation:** Uses other definitions and extracted keywords as incorrect options.

## Optional AI Mode

Copy `.env.example` to `.env` and add your key:

```env
OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o-mini
```

Then choose **AI Mode** while generating. If the API is unavailable or no key is present, the app automatically falls back to the local NLP engine.

## Security Features

- Upload extension validation for TXT, PDF, and DOCX.
- 10 MB upload-size limit.
- Filename sanitization using `secure_filename`.
- Uploaded files are parsed, then deleted.
- Uploaded content is never executed.
- SQL queries use parameterized statements.
- Flask/Jinja automatically escapes displayed text.
- No API keys are hard-coded.

## Limitations

- Local NLP is rule-based, so question quality depends on note clarity and grammar.
- Scanned/image-only PDFs cannot be parsed without OCR.
- AI Mode requires internet access and an API key.

## Future Enhancements

- OCR support for scanned PDFs.
- Spaced repetition and revision scheduling.
- User login and multi-user accounts.
- Export to Anki and PDF.
- Semantic question generation using local transformer models.
