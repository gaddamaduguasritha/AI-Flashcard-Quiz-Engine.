import os
import json
import re
import requests

DEFAULT_BASE_URL = "https://api.openai.com/v1"
DEFAULT_MODEL = "gpt-4o-mini"


def _build_prompt(text, card_count, question_count, difficulty):
    return f"""You are an educational AI that creates study material from lecture notes.

Create exactly {card_count} flashcards and exactly {question_count} quiz questions
from the lecture notes below. Every item must be directly based on the notes.

Difficulty: {difficulty}.

Return ONLY valid JSON in this exact structure:
{{
  "flashcards": [
    {{"front": "Question or term", "back": "Answer or explanation"}}
  ],
  "questions": [
    {{
      "type": "mcq",
      "question": "Question text",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correct": "Exact text of the correct option",
      "explanation": "Short explanation"
    }},
    {{
      "type": "true_false",
      "question": "True or False: statement",
      "options": ["True", "False"],
      "correct": "True",
      "explanation": "Short explanation"
    }}
  ]
}}

Lecture notes:
{text[:12000]}
"""


def generate_ai_study_material(text, card_count, question_count, difficulty):
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        return None

    base_url = os.environ.get("OPENAI_BASE_URL", DEFAULT_BASE_URL).rstrip("/")
    model = os.environ.get("OPENAI_MODEL", DEFAULT_MODEL)
    url = f"{base_url}/chat/completions"

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You create accurate study material as strict JSON."},
            {"role": "user", "content": _build_prompt(text, card_count, question_count, difficulty)},
        ],
        "temperature": 0.3,
        "response_format": {"type": "json_object"},
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        content = re.sub(r"^```json|```$", "", content.strip(), flags=re.MULTILINE).strip()
        data = json.loads(content)
    except Exception:
        return None

    flashcards = []
    for card in data.get("flashcards", [])[:card_count]:
        if isinstance(card, dict) and card.get("front") and card.get("back"):
            flashcards.append({"front": str(card["front"]), "back": str(card["back"])})

    questions = []
    for question in data.get("questions", [])[:question_count]:
        if not isinstance(question, dict):
            continue
        options = question.get("options")
        correct = question.get("correct")
        if not question.get("question") or not isinstance(options, list) or not correct:
            continue
        if question.get("type") == "true_false":
            options = ["True", "False"]
            if correct not in options:
                continue
        elif len(options) < 2 or correct not in options:
            continue
        questions.append({
            "type": "true_false" if question.get("type") == "true_false" else "mcq",
            "question": str(question["question"]),
            "options": [str(option) for option in options],
            "correct": str(correct),
            "explanation": str(question.get("explanation", "Based on the provided lecture notes.")),
        })

    if not flashcards or not questions:
        return None
    return {"flashcards": flashcards, "questions": questions}
