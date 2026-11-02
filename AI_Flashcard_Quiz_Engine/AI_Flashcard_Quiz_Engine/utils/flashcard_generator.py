import random

from utils.text_processor import (split_sentences, extract_keywords,
                                  detect_definitions, rank_sentences)


def _make_definition_cards(definitions):
    cards = []
    for item in definitions:
        term = item["term"].strip(" .,:;")
        definition = item["definition"].strip()
        if len(term) < 3 or len(definition) < 15:
            continue
        cards.append({
            "front": f"What is {term}?",
            "back": definition,
        })
    return cards


def _make_cloze_cards(sentences, keywords):
    cards = []
    seen = set()
    for sentence in sentences:
        for keyword in keywords:
            pattern = r"\b" + keyword + r"\b"
            if not __import__("re").search(pattern, sentence, flags=__import__("re").IGNORECASE):
                continue
            front = __import__("re").sub(
                pattern, "_______", sentence, count=1, flags=__import__("re").IGNORECASE
            )
            key = front.lower()
            if key in seen or front == sentence:
                continue
            seen.add(key)
            cards.append({
                "front": f"Fill in the blank: {front}",
                "back": keyword.capitalize(),
            })
            break
    return cards


def _make_concept_cards(sentences, keywords):
    cards = []
    for keyword in keywords:
        related = [sentence for sentence in sentences
                   if keyword in sentence.lower()]
        if not related:
            continue
        best_sentence = related[0]
        cards.append({
            "front": f"Explain the concept: {keyword.capitalize()}",
            "back": best_sentence,
        })
    return cards


def generate_flashcards(text, count=10):
    count = max(5, min(20, int(count)))
    sentences = split_sentences(text)
    keywords = extract_keywords(text)
    definitions = detect_definitions(sentences)
    important_sentences = rank_sentences(sentences, keywords, limit=60)

    cards = _make_definition_cards(definitions)
    cards += _make_cloze_cards(important_sentences, keywords)
    cards += _make_concept_cards(important_sentences, keywords)

    unique_cards = []
    seen_fronts = set()
    for card in cards:
        key = card["front"].lower().strip()
        if key not in seen_fronts and card["back"].strip():
            unique_cards.append(card)
            seen_fronts.add(key)

    random.shuffle(unique_cards)
    if len(unique_cards) < count:
        for sentence in important_sentences:
            if len(unique_cards) >= count:
                break
            card = {
                "front": "Which statement is important in these lecture notes?",
                "back": sentence,
            }
            if card["back"].lower() not in seen_fronts:
                unique_cards.append(card)
                seen_fronts.add(card["back"].lower())

    return unique_cards[:count]
