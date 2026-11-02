import re
from collections import Counter

STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "if", "then", "than", "that", "this",
    "these", "those", "is", "are", "was", "were", "be", "been", "being", "to",
    "of", "in", "on", "at", "by", "for", "with", "about", "as", "into", "from",
    "it", "its", "they", "them", "their", "we", "our", "you", "your", "he",
    "she", "his", "her", "not", "no", "can", "could", "will", "would", "should",
    "may", "might", "must", "do", "does", "did", "have", "has", "had", "which",
    "who", "whom", "what", "when", "where", "why", "how", "also", "such", "some",
    "any", "each", "other", "more", "most", "many", "much", "between", "because",
    "while", "during", "there", "here", "one", "two", "using", "used", "use"
}


def clean_text(text):
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[\u0000-\u0008\u000b\u000c\u000e-\u001f]", " ", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def split_sentences(text):
    text = clean_text(text)
    text = re.sub(r"\n+", " ", text)
    sentences = re.split(r"(?<=[.!?])\s+", text)
    result = []
    for sentence in sentences:
        sentence = sentence.strip()
        words = sentence.split()
        if 6 <= len(words) <= 60 and not sentence.endswith((":", ";", ",")):
            result.append(sentence)
    return result


def extract_keywords(text, limit=30):
    words = re.findall(r"[A-Za-z][A-Za-z\-']{2,}", text)
    filtered = []
    for word in words:
        lowered = word.lower()
        if lowered not in STOPWORDS and not lowered.isdigit():
            filtered.append(lowered)
    counts = Counter(filtered)
    keywords = []
    for word, count in counts.most_common(limit * 2):
        if count > 1 and word not in keywords:
            keywords.append(word)
        if len(keywords) >= limit:
            break
    return keywords


def detect_definitions(sentences):
    pattern = re.compile(
        r"^(.{2,70}?)\s+(?:is|are|refers to|means|is defined as|are defined as)\s+(.{15,400}?)[.?!]?$",
        re.IGNORECASE,
    )
    definitions = []
    seen_terms = set()
    for sentence in sentences:
        match = pattern.match(sentence)
        if not match:
            continue
        term = match.group(1).strip()
        definition = match.group(2).strip()
        term_key = term.lower()
        if term_key in seen_terms or len(term.split()) > 8:
            continue
        seen_terms.add(term_key)
        definitions.append({"term": term, "definition": definition, "sentence": sentence})
    return definitions


def rank_sentences(sentences, keywords, limit=30):
    keyword_set = set(keywords)
    ranked = []
    for index, sentence in enumerate(sentences):
        words = re.findall(r"[A-Za-z][A-Za-z\-']{2,}", sentence.lower())
        if not words:
            continue
        keyword_hits = sum(1 for word in words if word in keyword_set)
        length_score = min(len(words), 35) / 35
        position_score = 1 - (index / max(len(sentences), 1)) * 0.3
        score = keyword_hits * 2 + length_score + position_score
        ranked.append((score, index, sentence))
    ranked.sort(reverse=True)
    return [item[2] for item in ranked[:limit]]


def split_sections(text, max_characters=1500):
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    sections = []
    current = ""
    for paragraph in paragraphs:
        if len(current) + len(paragraph) + 2 <= max_characters:
            current = f"{current}\n\n{paragraph}".strip()
        else:
            if current:
                sections.append(current)
            current = paragraph
    if current:
        sections.append(current)
    return sections
