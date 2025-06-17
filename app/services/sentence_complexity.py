import nltk
from nltk import tokenize
from statistics import mean, variance

# Ensure required NLTK corpora

def _ensure_nltk_data():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)

_ensure_nltk_data()

def analyze_sentence_complexity(text: str) -> dict:
    """Compute sentence complexity metrics.

    Args:
        text (str): Input text

    Returns:
        dict: Average sentence length, variance, sentence count, word count
    """
    if not text or not isinstance(text, str):
        return {
            'sentence_count': 0,
            'word_count': 0,
            'average_sentence_length': 0.0,
            'sentence_length_variance': 0.0
        }

    sentences = tokenize.sent_tokenize(text)
    sentence_lengths = [len(tokenize.word_tokenize(s)) for s in sentences if s.strip()]

    if not sentence_lengths:
        return {
            'sentence_count': 0,
            'word_count': 0,
            'average_sentence_length': 0.0,
            'sentence_length_variance': 0.0
        }

    avg_len = mean(sentence_lengths)
    var_len = variance(sentence_lengths) if len(sentence_lengths) > 1 else 0.0

    return {
        'sentence_count': len(sentence_lengths),
        'word_count': sum(sentence_lengths),
        'average_sentence_length': round(avg_len, 2),
        'sentence_length_variance': round(var_len, 2)
    } 