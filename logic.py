import spacy

try:
    nlp = spacy.load("uk_core_news_sm")
except OSError:
    print("Модель не знайдено. Виконайте: python -m spacy download uk_core_news_sm")

TENSE_MAP = {
    "Past": "Минулий",
    "Pres": "Теперішній",
    "Fut": "Майбутній",
    "-": "Не визначено"
}

GENDER_MAP = {
    "Masc": "Чоловічий",
    "Fem": "Жіночий",
    "Neut": "Середній",
    "-": "Не визначено"
}

NUMBER_MAP = {
    "Sing": "Однина",
    "Plur": "Множина",
    "-": "Не визначено"
}

ASPECT_MAP = {
    "Perf": "Доконаний",
    "Imp": "Недоконаний",
    "-": "Не визначено"
}

POS_MAP = {
    "NOUN": "ІМЕННИК",
    "VERB": "ДІЄСЛОВО",
    "ADJ": "ПРИКМЕТНИК",
    "ADV": "ПРИСЛІВНИК",
    "PRON": "ЗАЙМЕННИК",
    "DET": "ЗАЙМЕННИК",
    "ADP": "ПРИЙМЕННИК",
    "CCONJ": "СПОЛУЧНИК",
    "NUM": "ЧИСЛІВНИК",
    "PART": "ЧАСТКА",
    "INTJ": "ВИГУК",
    "X": "ІНШЕ"
}

def analyze_text(text):
    if not text:
        return None
    return nlp(text)

def get_verbs(doc):
    verbs = []
    for token in doc:
        if token.pos_ == "VERB":
            verbs.append({
                "word": token.text,
                "lemma": token.lemma_,
                "index": token.i
            })
    return verbs

def get_verb_morphology(token):
    morph = token.morph.to_dict()
    
    tense = TENSE_MAP.get(morph.get("Tense", "-"), morph.get("Tense", "-"))
    gender = GENDER_MAP.get(morph.get("Gender", "-"), morph.get("Gender", "-"))
    number = NUMBER_MAP.get(morph.get("Number", "-"), morph.get("Number", "-"))
    aspect = ASPECT_MAP.get(morph.get("Aspect", "-"), morph.get("Aspect", "-"))
    
    return {
        "Час": tense,
        "Рід": gender,
        "Число": number,
        "Вид": aspect
    }

def sentence_to_pos(doc, sentence_index):
    sentences = list(doc.sents)
    if sentence_index < 0 or sentence_index >= len(sentences):
        return None, "Невірний номер речення"
    
    target_sentence = sentences[sentence_index]
    pos_sentence = []
    
    for token in target_sentence:
        if token.pos_ != "PUNCT":
            pos_tag_ua = POS_MAP.get(token.pos_, token.pos_)
            pos_sentence.append(f"{pos_tag_ua}")
        else:
            pos_sentence.append(token.text)
            
    return target_sentence.text, " ".join(pos_sentence)