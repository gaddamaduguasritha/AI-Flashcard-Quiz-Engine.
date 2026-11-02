import os
import json
import sqlite3
from datetime import datetime
from flask import (Flask, render_template, request, redirect, url_for,
                   flash, abort, send_file, jsonify)
from werkzeug.utils import secure_filename

from utils.database import init_db, get_db
from utils.file_parser import extract_text, ALLOWED_EXTENSIONS
from utils.text_processor import clean_text
from utils.flashcard_generator import generate_flashcards
from utils.quiz_generator import generate_quiz
from utils.ai_client import generate_ai_study_material

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
DB_PATH = os.path.join(BASE_DIR, "database", "app.db")
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "college-project-secret-key")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "database"), exist_ok=True)
init_db(DB_PATH)


def safe_int(value, default, minimum, maximum):
    try:
        number = int(value)
    except (TypeError, ValueError):
        return default
    return max(minimum, min(maximum, number))


def save_uploaded_file(file_storage):
    if not file_storage or not file_storage.filename:
        return None, "Please choose a file to upload."
    filename = secure_filename(file_storage.filename)
    if "." not in filename:
        return None, "Unsupported file type."
    extension = filename.rsplit(".", 1)[1].lower()
    if extension not in ALLOWED_EXTENSIONS:
        return None, "Unsupported file type. Allowed: TXT, PDF and DOCX."
    unique_name = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{filename}"
    path = os.path.join(app.config["UPLOAD_FOLDER"], unique_name)
    file_storage.save(path)
    return path, None


def create_study_material(note_id, text, title, card_count, question_count, difficulty, mode):
    ai_result = None
    if mode == "ai":
        ai_result = generate_ai_study_material(text, card_count, question_count, difficulty)

    if ai_result:
        flashcards = ai_result["flashcards"]
        questions = ai_result["questions"]
        generator_mode = "ai"
    else:
        flashcards = generate_flashcards(text, card_count)
        questions = generate_quiz(text, question_count, difficulty)
        generator_mode = "local"

    db = get_db(DB_PATH)
    db.execute("DELETE FROM flashcards WHERE note_id = ?", (note_id,))
    db.execute("DELETE FROM quiz_questions WHERE quiz_id IN (SELECT id FROM quizzes WHERE note_id = ?)", (note_id,))
    db.execute("DELETE FROM quizzes WHERE note_id = ?", (note_id,))
    db.execute("DELETE FROM quiz_attempts WHERE quiz_id IN (SELECT id FROM quizzes WHERE note_id = ?)", (note_id,))

    for index, card in enumerate(flashcards):
        db.execute(
            "INSERT INTO flashcards (note_id, front, back, position) VALUES (?, ?, ?, ?)",
            (note_id, card["front"], card["back"], index),
        )

    cursor = db.execute(
        "INSERT INTO quizzes (note_id, difficulty, generator_mode, created_at) VALUES (?, ?, ?, ?)",
        (note_id, difficulty, generator_mode, datetime.utcnow().isoformat()),
    )
    quiz_id = cursor.lastrowid

    for index, question in enumerate(questions):
        db.execute(
            """INSERT INTO quiz_questions
               (quiz_id, question_type, question_text, options_json, correct_answer, explanation, position)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (quiz_id, question["type"], question["question"],
             json.dumps(question["options"]), question["correct"],
             question["explanation"], index),
        )

    db.execute("UPDATE notes SET generator_mode = ? WHERE id = ?", (generator_mode, note_id))
    db.commit()
    db.close()
    return quiz_id


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["GET", "POST"])
def generate():
    if request.method == "POST":
        title = request.form.get("title", "").strip() or "Untitled Lecture Notes"
        pasted_text = request.form.get("notes", "").strip()
        card_count = safe_int(request.form.get("card_count"), 10, 5, 20)
        question_count = safe_int(request.form.get("question_count"), 10, 5, 20)
        difficulty = request.form.get("difficulty", "medium").lower()
        mode = request.form.get("mode", "local").lower()

        if difficulty not in ("easy", "medium", "hard"):
            difficulty = "medium"
        if mode not in ("local", "ai"):
            mode = "local"

        uploaded_path, upload_error = save_uploaded_file(request.files.get("file"))
        if upload_error:
            flash(upload_error, "danger")
            return render_template("generate.html", form=request.form)

        if uploaded_path:
            try:
                extracted, parse_error = extract_text(uploaded_path)
            except Exception:
                extracted, parse_error = "", "The uploaded file could not be read."
            finally:
                try:
                    os.remove(uploaded_path)
                except OSError:
                    pass
            if parse_error:
                flash(parse_error, "danger")
                return render_template("generate.html", form=request.form)
            text = extracted
            source_type = "upload"
        else:
            text = pasted_text
            source_type = "paste"

        text = clean_text(text)
        if len(text.split()) < 40:
            flash("Please provide at least 40 words of lecture notes.", "warning")
            return render_template("generate.html", form=request.form)

        db = get_db(DB_PATH)
        cursor = db.execute(
            "INSERT INTO notes (title, source_type, content, generator_mode, created_at) VALUES (?, ?, ?, ?, ?)",
            (title, source_type, text, "local", datetime.utcnow().isoformat()),
        )
        note_id = cursor.lastrowid
        db.commit()
        db.close()

        try:
            create_study_material(note_id, text, title, card_count, question_count, difficulty, mode)
        except Exception as exc:
            flash(f"Study material could not be generated: {exc}", "danger")
            return redirect(url_for("generate"))

        flash("Flashcards and quiz generated successfully.", "success")
        return redirect(url_for("flashcards", note_id=note_id))

    return render_template("generate.html", form={})


@app.route("/flashcards/<int:note_id>")
def flashcards(note_id):
    db = get_db(DB_PATH)
    note = db.execute("SELECT * FROM notes WHERE id = ?", (note_id,)).fetchone()
    if not note:
        db.close()
        abort(404)
    cards = db.execute(
        "SELECT * FROM flashcards WHERE note_id = ? ORDER BY position", (note_id,)
    ).fetchall()
    quiz = db.execute(
        "SELECT * FROM quizzes WHERE note_id = ? ORDER BY id DESC LIMIT 1", (note_id,)
    ).fetchone()
    db.close()
    if not cards:
        flash("No flashcards were generated for these notes.", "warning")
    return render_template("flashcards.html", note=note, cards=cards, quiz=quiz)


@app.route("/quiz/<int:note_id>")
def quiz(note_id):
    db = get_db(DB_PATH)
    note = db.execute("SELECT * FROM notes WHERE id = ?", (note_id,)).fetchone()
    if not note:
        db.close()
        abort(404)
    quiz_row = db.execute(
        "SELECT * FROM quizzes WHERE note_id = ? ORDER BY id DESC LIMIT 1", (note_id,)
    ).fetchone()
    if not quiz_row:
        db.close()
        flash("No quiz has been generated for these notes yet.", "warning")
        return redirect(url_for("flashcards", note_id=note_id))
    questions = db.execute(
        "SELECT * FROM quiz_questions WHERE quiz_id = ? ORDER BY position", (quiz_row["id"],)
    ).fetchall()
    db.close()
    parsed = []
    for question in questions:
        item = dict(question)
        item["options"] = json.loads(question["options_json"])
        parsed.append(item)
    return render_template("quiz.html", note=note, quiz=quiz_row, questions=parsed)


@app.route("/quiz/<int:note_id>/submit", methods=["POST"])
def submit_quiz(note_id):
    db = get_db(DB_PATH)
    quiz_row = db.execute(
        "SELECT * FROM quizzes WHERE note_id = ? ORDER BY id DESC LIMIT 1", (note_id,)
    ).fetchone()
    if not quiz_row:
        db.close()
        abort(404)
    questions = db.execute(
        "SELECT * FROM quiz_questions WHERE quiz_id = ? ORDER BY position", (quiz_row["id"],)
    ).fetchall()

    answers = {}
    score = 0
    for question in questions:
        selected = request.form.get(f"answer_{question['id']}", "").strip()
        answers[str(question["id"])] = selected
        if selected and selected == question["correct_answer"]:
            score += 1

    total = len(questions)
    percentage = round((score / total) * 100, 2) if total else 0
    cursor = db.execute(
        """INSERT INTO quiz_attempts
           (quiz_id, note_id, score, total, percentage, answers_json, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (quiz_row["id"], note_id, score, total, percentage,
         json.dumps(answers), datetime.utcnow().isoformat()),
    )
    attempt_id = cursor.lastrowid
    db.commit()
    db.close()
    return redirect(url_for("results", attempt_id=attempt_id))


@app.route("/results/<int:attempt_id>")
def results(attempt_id):
    db = get_db(DB_PATH)
    attempt = db.execute("SELECT * FROM quiz_attempts WHERE id = ?", (attempt_id,)).fetchone()
    if not attempt:
        db.close()
        abort(404)
    note = db.execute("SELECT * FROM notes WHERE id = ?", (attempt["note_id"],)).fetchone()
    questions = db.execute(
        """SELECT q.* FROM quiz_questions q
           WHERE q.quiz_id = ? ORDER BY q.position""",
        (attempt["quiz_id"],),
    ).fetchall()
    db.close()

    answers = json.loads(attempt["answers_json"])
    review = []
    for question in questions:
        selected = answers.get(str(question["id"]), "")
        review.append({
            "question": question,
            "options": json.loads(question["options_json"]),
            "selected": selected,
            "is_correct": selected == question["correct_answer"],
        })

    return render_template("results.html", attempt=attempt, note=note, review=review)


@app.route("/history")
def history():
    db = get_db(DB_PATH)
    notes = db.execute(
        """SELECT n.*, 
                  (SELECT COUNT(*) FROM flashcards f WHERE f.note_id = n.id) AS card_count,
                  (SELECT COUNT(*) FROM quiz_questions qq
                    JOIN quizzes qz ON qq.quiz_id = qz.id WHERE qz.note_id = n.id) AS question_count
           FROM notes n ORDER BY n.created_at DESC"""
    ).fetchall()
    attempts = db.execute(
        """SELECT a.*, n.title FROM quiz_attempts a
           JOIN notes n ON n.id = a.note_id ORDER BY a.created_at DESC LIMIT 50"""
    ).fetchall()
    db.close()
    return render_template("history.html", notes=notes, attempts=attempts)


@app.route("/notes/<int:note_id>")
def note_details(note_id):
    db = get_db(DB_PATH)
    note = db.execute("SELECT * FROM notes WHERE id = ?", (note_id,)).fetchone()
    if not note:
        db.close()
        abort(404)
    cards = db.execute(
        "SELECT COUNT(*) FROM flashcards WHERE note_id = ?", (note_id,)
    ).fetchone()[0]
    quiz_row = db.execute(
        "SELECT * FROM quizzes WHERE note_id = ? ORDER BY id DESC LIMIT 1", (note_id,)
    ).fetchone()
    question_count = 0
    if quiz_row:
        question_count = db.execute(
            "SELECT COUNT(*) FROM quiz_questions WHERE quiz_id = ?", (quiz_row["id"],)
        ).fetchone()[0]
    db.close()
    return render_template("note_details.html", note=note, cards=cards,
                           quiz=quiz_row, question_count=question_count)


@app.route("/notes/<int:note_id>/regenerate", methods=["POST"])
def regenerate(note_id):
    db = get_db(DB_PATH)
    note = db.execute("SELECT * FROM notes WHERE id = ?", (note_id,)).fetchone()
    db.close()
    if not note:
        abort(404)
    card_count = safe_int(request.form.get("card_count"), 10, 5, 20)
    question_count = safe_int(request.form.get("question_count"), 10, 5, 20)
    difficulty = request.form.get("difficulty", "medium").lower()
    mode = request.form.get("mode", "local").lower()
    if difficulty not in ("easy", "medium", "hard"):
        difficulty = "medium"
    if mode not in ("local", "ai"):
        mode = "local"
    create_study_material(note_id, note["content"], note["title"],
                          card_count, question_count, difficulty, mode)
    flash("Study material regenerated successfully.", "success")
    return redirect(url_for("flashcards", note_id=note_id))


@app.route("/download/flashcards/<int:note_id>")
def download_flashcards(note_id):
    export_format = request.args.get("format", "txt").lower()
    db = get_db(DB_PATH)
    note = db.execute("SELECT * FROM notes WHERE id = ?", (note_id,)).fetchone()
    cards = db.execute(
        "SELECT front, back FROM flashcards WHERE note_id = ? ORDER BY position", (note_id,)
    ).fetchall()
    db.close()
    if not note or not cards:
        abort(404)

    safe_title = "".join(c if c.isalnum() else "_" for c in note["title"])[:50] or "flashcards"
    if export_format == "json":
        path = os.path.join(app.config["UPLOAD_FOLDER"], f"{safe_title}_flashcards.json")
        with open(path, "w", encoding="utf-8") as handle:
            json.dump([dict(card) for card in cards], handle, indent=2, ensure_ascii=False)
        mimetype = "application/json"
    else:
        path = os.path.join(app.config["UPLOAD_FOLDER"], f"{safe_title}_flashcards.txt")
        with open(path, "w", encoding="utf-8") as handle:
            for index, card in enumerate(cards, 1):
                handle.write(f"Flashcard {index}\n")
                handle.write(f"FRONT: {card['front']}\n")
                handle.write(f"BACK: {card['back']}\n\n")
        mimetype = "text/plain"
    return send_file(path, as_attachment=True)


@app.route("/download/results/<int:attempt_id>")
def download_results(attempt_id):
    db = get_db(DB_PATH)
    attempt = db.execute("SELECT * FROM quiz_attempts WHERE id = ?", (attempt_id,)).fetchone()
    if not attempt:
        db.close()
        abort(404)
    note = db.execute("SELECT title FROM notes WHERE id = ?", (attempt["note_id"],)).fetchone()
    questions = db.execute(
        "SELECT * FROM quiz_questions WHERE quiz_id = ? ORDER BY position",
        (attempt["quiz_id"],),
    ).fetchall()
    db.close()

    answers = json.loads(attempt["answers_json"])
    safe_title = "".join(c if c.isalnum() else "_" for c in note["title"])[:50] or "quiz"
    path = os.path.join(app.config["UPLOAD_FOLDER"], f"{safe_title}_results.txt")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(f"Quiz Result - {note['title']}\n")
        handle.write(f"Score: {attempt['score']}/{attempt['total']}\n")
        handle.write(f"Percentage: {attempt['percentage']}%\n\n")
        for index, question in enumerate(questions, 1):
            selected = answers.get(str(question["id"]), "Not answered")
            handle.write(f"Q{index}. {question['question_text']}\n")
            handle.write(f"Your answer: {selected}\n")
            handle.write(f"Correct answer: {question['correct_answer']}\n")
            handle.write(f"Explanation: {question['explanation']}\n\n")
    return send_file(path, as_attachment=True)


@app.route("/about")
def about():
    return render_template("about.html")


@app.errorhandler(404)
def page_not_found(error):
    return render_template("error.html", code=404, message="Page not found."), 404


@app.errorhandler(413)
def file_too_large(error):
    return render_template("error.html", code=413,
                           message="Uploaded file is too large. Maximum size is 10 MB."), 413


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
