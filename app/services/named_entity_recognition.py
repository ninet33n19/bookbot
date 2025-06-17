import spacy

# Ensure spaCy model is available

def _ensure_spacy_model():
    try:
        return spacy.load('en_core_web_sm')
    except OSError:
        from spacy.cli import download
        download('en_core_web_sm')
        return spacy.load('en_core_web_sm')

_nlp = _ensure_spacy_model()


def analyze_named_entities(text: str) -> dict:
    """Extract named entities from text.

    Args:
        text (str): Input text

    Returns:
        dict: Entities grouped by label
    """
    if not text or not isinstance(text, str):
        return {'entities': {}}

    doc = _nlp(text)
    entities_by_label = {}
    for ent in doc.ents:
        entities_by_label.setdefault(ent.label_, []).append(ent.text)

    # Deduplicate entity text per label
    for label in entities_by_label:
        entities_by_label[label] = list(set(entities_by_label[label]))

    return {'entities': entities_by_label} 