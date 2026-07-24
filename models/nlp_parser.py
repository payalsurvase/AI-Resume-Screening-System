import spacy

# Load spaCy model only once
nlp = spacy.load("en_core_web_sm")


def parse_resume_nlp(text):
    """
    Parse resume using spaCy NLP
    """

    doc = nlp(text)

    entities = []

    for ent in doc.ents:
        entities.append({
            "text": ent.text,
            "label": ent.label_
        })

    return entities