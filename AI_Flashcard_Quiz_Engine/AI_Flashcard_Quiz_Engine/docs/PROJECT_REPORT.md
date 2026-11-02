# Project Report

## Title

AI Flashcard and Quiz Engine from Lecture Notes

## Abstract

The project is a Flask-based intelligent study tool that automatically converts lecture notes into flashcards and quizzes. Students can paste notes or upload TXT, PDF, and DOCX files. The system extracts text, identifies key concepts and definitions, ranks important sentences, and generates interactive study material. It works offline using local NLP techniques and optionally supports an external AI API.

## Introduction

Revision is an essential part of learning, but creating flashcards and practice questions manually is time-consuming. This project automates that process by analyzing lecture notes and producing interactive revision content.

## Problem Statement

Students possess large amounts of lecture material but lack time to prepare structured revision resources. Manual question creation is repetitive, inconsistent, and often incomplete.

## Existing System

In traditional study methods, students manually highlight notes, write flashcards, and create questions. This requires considerable time and does not provide automatic scoring or explanations.

## Proposed System

The proposed system automatically processes lecture notes and generates flashcards, MCQs, true/false questions, quiz scores, and explanations. It stores all study sessions in SQLite and allows students to revisit previous material.

## Objectives

- Automate flashcard and quiz creation.
- Support TXT, PDF, and DOCX inputs.
- Operate without a paid AI API.
- Provide interactive flashcard and quiz interfaces.
- Store and display study history.
- Provide quiz scoring and answer explanations.

## Requirements

### Functional Requirements

- Paste or upload lecture notes.
- Extract text from TXT, PDF, and DOCX.
- Generate 5 to 20 flashcards.
- Generate 5 to 20 quiz questions.
- Support easy, medium, and hard difficulty.
- Calculate score, percentage, correct answers, and incorrect answers.
- Store notes, flashcards, quizzes, and attempts.
- Export flashcards and quiz results.

### Non-Functional Requirements

- Responsive user interface.
- Secure file-upload validation.
- Local execution without mandatory internet access.
- Simple installation and usage.

## System Architecture

1. **Presentation Layer:** HTML, CSS, JavaScript, Bootstrap.
2. **Application Layer:** Flask routes, validation, session control.
3. **AI/NLP Layer:** Text processing, flashcard generation, quiz generation, optional AI client.
4. **Data Layer:** SQLite database.
5. **File Layer:** Temporary upload parsing and export-file generation.

## Modules

- User interface module
- File upload and parsing module
- Text-processing module
- Flashcard-generation module
- Quiz-generation module
- Quiz evaluation module
- Database module
- History and export module
- Optional AI integration module

## Database Design

The database contains five related tables: `notes`, `flashcards`, `quizzes`, `quiz_questions`, and `quiz_attempts`. Foreign keys connect flashcards to notes, questions to quizzes, and attempts to both quizzes and notes.

## AI/NLP Methodology

The local engine applies text cleaning, sentence splitting, stop-word removal, keyword-frequency analysis, definition-pattern matching, sentence ranking, cloze generation, distractor selection, and rule-based true/false generation.

## Implementation

Flask handles routing and form handling. SQLite stores persistent data. Jinja templates render pages. Bootstrap provides responsive layout. JavaScript controls flashcard flipping, shuffling, quiz option selection, and progress display.

## Testing

The application was tested for text extraction, empty-input validation, invalid file types, oversized uploads, flashcard generation, quiz generation, scoring, database persistence, exports, and responsive layout.

## Results

The system successfully converts structured lecture notes into relevant flashcards and quizzes. It provides immediate scoring and explanation-based review.

## Advantages

- Saves revision time.
- Works offline.
- Low hardware requirement.
- Simple to install and demonstrate.
- Provides measurable quiz feedback.

## Limitations

- Local generation is rule-based rather than deeply semantic.
- Scanned PDFs require OCR.
- AI mode needs an external API key and internet connection.

## Future Scope

- OCR integration.
- User authentication.
- Spaced repetition.
- Anki/PDF export.
- Local transformer-based question generation.

## Conclusion

The project demonstrates a practical AI-enabled educational application that converts lecture notes into interactive study material using accessible technologies.

## References

- Flask documentation: https://flask.palletsprojects.com/
- SQLite documentation: https://www.sqlite.org/docs.html
- Bootstrap documentation: https://getbootstrap.com/docs/
- PyPDF2 documentation: https://pypdf2.readthedocs.io/
- python-docx documentation: https://python-docx.readthedocs.io/
