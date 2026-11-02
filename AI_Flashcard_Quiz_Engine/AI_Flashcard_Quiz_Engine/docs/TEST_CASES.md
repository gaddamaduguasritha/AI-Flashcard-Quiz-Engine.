# Test Cases

| Test Case ID | Feature | Input | Expected Output | Actual Output | Status |
|---|---|---|---|---|---|
| TC01 | Home page | Open `http://127.0.0.1:5000` | Home page loads with Get Started button | Home page loads correctly | Pass |
| TC02 | Paste notes | Paste sample AI notes | Notes accepted for generation | Notes accepted | Pass |
| TC03 | TXT upload | Upload valid `.txt` file | Text extracted successfully | Text extracted | Pass |
| TC04 | PDF upload | Upload text-based `.pdf` | Text extracted successfully | Text extracted | Pass |
| TC05 | DOCX upload | Upload valid `.docx` | Text extracted successfully | Text extracted | Pass |
| TC06 | Invalid file | Upload `.exe` | Error: unsupported file type | Error displayed | Pass |
| TC07 | Empty notes | Submit empty form | Warning asking for at least 40 words | Warning displayed | Pass |
| TC08 | Short notes | Submit 10 words | Warning displayed | Warning displayed | Pass |
| TC09 | Flashcard generation | Select 10 flashcards | 10 relevant flashcards created | 10 flashcards created | Pass |
| TC10 | Flashcard flip | Click flashcard | Card flips to show answer | Card flips | Pass |
| TC11 | Flashcard shuffle | Click Shuffle | Card order changes | Order changes | Pass |
| TC12 | Flashcard navigation | Click Previous/Next | Correct card displayed | Navigation works | Pass |
| TC13 | Quiz generation | Select 10 questions | MCQs and/or true/false questions generated | Questions generated | Pass |
| TC14 | Quiz answering | Select answers | Selection highlighted and progress updates | Works correctly | Pass |
| TC15 | Quiz submission | Submit completed quiz | Redirect to result page | Redirects correctly | Pass |
| TC16 | Score calculation | Answer 8 of 10 correctly | Score 8/10, 80% | Correct score shown | Pass |
| TC17 | Answer review | Open result page | Correct/incorrect status and explanations shown | Review displayed | Pass |
| TC18 | History | Generate and attempt quiz | Session and attempt appear in History | Records displayed | Pass |
| TC19 | Flashcard TXT export | Click TXT download | TXT file downloads | File downloads | Pass |
| TC20 | Flashcard JSON export | Click JSON download | JSON file downloads | File downloads | Pass |
| TC21 | Result download | Click Download Results | Result TXT downloads | File downloads | Pass |
| TC22 | Regeneration | Click Regenerate | New flashcards and quiz generated | Material regenerated | Pass |
| TC23 | Database initialization | Start app first time | `database/app.db` created | Database created | Pass |
| TC24 | Missing page | Open invalid URL | 404 error page displayed | 404 page displayed | Pass |
| TC25 | Oversized upload | Upload file above 10 MB | 413 error page displayed | Error handled | Pass |
