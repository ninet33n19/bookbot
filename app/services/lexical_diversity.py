import nltk
from nltk import tokenize
from collections import Counter

# Ensure NLTK data

def _ensure_nltk_data():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)

_ensure_nltk_data()

def analyze_lexical_diversity(text: str) -> dict:
    """Compute lexical diversity metrics (TTR, hapax legomena, etc.).

    Args:
        text (str): Input text

    Returns:
        dict: Lexical diversity statistics
    """
    if not text or not isinstance(text, str):
        return {
            'token_count': 0,
            'type_count': 0,
            'type_token_ratio': 0.0,
            'hapax_legomena_count': 0
        }

    tokens = [t.lower() for t in tokenize.word_tokenize(text) if t.isalpha()]
    token_count = len(tokens)
    if token_count == 0:
        return {
            'token_count': 0,
            'type_count': 0,
            'type_token_ratio': 0.0,
            'hapax_legomena_count': 0
        }

    type_count = len(set(tokens))
    ttr = type_count / token_count

    freq_dist = Counter(tokens)
    hapax_legomena_count = sum(1 for w, c in freq_dist.items() if c == 1)

    return {
        'token_count': token_count,
        'type_count': type_count,
        'type_token_ratio': round(ttr, 3),
        'hapax_legomena_count': hapax_legomena_count
    } 