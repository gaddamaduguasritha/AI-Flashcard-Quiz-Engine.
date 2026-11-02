import random
import re

from utils.text_processor import (split_sentences, extract_keywords,
                                  detect_definitions, rank_sentences)


def _truncate(text, limit=140):
    text = text.strip()
    return text if len(text) <= limit else text[:limit].rsplit(" ", 1)[0] + "..."


def _definition_mcqs(definitions, count):
    questions = []
    for item in definitions:
        if len(questions) >= count:
            break
        correct = _truncate(item["definition"])
        distractors = []
        for other in definitions:
            if other["term"].lower() == item["term"].lower():
                continue
            option = _truncate(other["definition"])
            if option != correct and option not in distractors:
                distractors.append(option)
        if len(distractors) < 3:
            continue
        options = [correct] + distractors[:3]
        random.shuffle(options)
        questions.append({
            "type": "mcq",
            "question": f"What is {item['term'].strip(' .,:;')}?",
            "options": options,
            "correct": correct,
            "explanation": item["sentence"],
        })
    return questions


def _keyword_mcqs(sentences, keywords, count):
    questions = []
    used_sentences = set()
    for sentence in sentences:
        if len(questions) >= count:
            break
        sentence_key = sentence.lower()
        if sentence_key in used_sentences:
            continue
        target = None
        for keyword in keywords:
            if re.search(r"\b" + keyword + r"\b", sentence, flags=re.IGNORECASE):
                target = keyword
                break
        if not target:
            continue
        distractors = [word for word in keywords if word != target][:10]
        random.shuffle(distractors)
        if len(distractors) < 3:
            continue
        options = [target] + distractors[:3]
        random.shuffle(options)
        question_text = re.sub(
            r"\b" + target + r"\b", "_______", sentence, count=1, flags=re.IGNORECASE
        )
        questions.append({
            "type": "mcq",
            "question": f"Fill in the blank: {question_text}",
            "options": options,
            "correct": target,
            "explanation": f"The correct term is '{target}'. Original statement: {sentence}",
        })
        used_sentences.add(sentence_key)
    return questions


def _true_false_questions(sentences, keywords, count):
    questions = []
    candidates = [s for s in sentences if any(k in s.lower() for k in keywords)]
    random.shuffle(candidates)
    for index, sentence in enumerate(candidates):
        if len(questions) >= count:
            break
        target = None
        for keyword in keywords:
            if re.search(r"\b" + keyword + r"\b", sentence, flags=re.IGNORECASE):
                target = keyword
                break
        if not target:
            continue
        make_false = index % 2 == 1
        if make_false:
            replacement = next((k for k in keywords if k != target), None)
            if not replacement:
                continue
            statement = re.sub(
                r"\b" + target + r"\b", replacement, sentence, count=1,
                flags=re.IGNORECASE,
            )
            correct = "False"
            explanation = f"The original lecture note says: {sentence}"
        else:
            statement = sentence
            correct = "True"
            explanation = "This statement is taken directly from the lecture notes."
        questions.append({
            "type": "true_false",
            "question": f"True or False: {statement}",
            "options": ["True", "False"],
            "correct": correct,
            "explanation": explanation,
        })
    return questions


def generate_quiz(text, count=10, difficulty="medium"):
    count = max(5, min(20, int(count)))
    difficulty = difficulty if difficulty in ("easy", "medium", "hard") else "medium"

    sentences = split_sentences(text)
    keywords = extract_keywords(text)
    definitions = detect_definitions(sentences)
    important_sentences = rank_sentences(sentences, keywords, limit=60)

    if difficulty == "easy":
        definition_count = max(2, count // 2)
        keyword_count = count - definition_count
        true_false_count = 0
    elif difficulty == "medium":
        definition_count = max(1, count // 3)
        keyword_count = max(1, count // 2)
        true_false_count = count - definition_count - keyword_count
    else:
        definition_count = max(1, count // 4)
        keyword_count = max(1, count // 2)
        true_false_count = count - definition_count - keyword_count

    questions = []
    questions += _definition_mcqs(definitions, definition_count)
    questions += _keyword_mcqs(important_sentences, keywords, keyword_count)
    questions += _true_false_questions(important_sentences, keywords, true_false_count)

    if len(questions) < count:
        questions += _keyword_mcqs(important_sentences, keywords, count - len(questions))
    if len(questions) < count:
        questions += _true_false_questions(important_sentences, keywords, count - len(questions))

    unique_questions = []
    seen = set()
    for question in questions:
        key = question["question"].lower()
        if key not in seen:
            unique_questions.append(question)
            seen.add(key)

    random.shuffle(unique_questions)
    return unique_questions[:count]
