from rake_nltk import Rake

# Ensure required NLTK data for RAKE (stopwords/punkt)
import nltk

def _ensure_nltk_data():
    for resource in ['punkt', 'stopwords']:
        try:
            nltk.data.find(f'tokenizers/{resource}') if resource == 'punkt' else nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download(resource, quiet=True)

_ensure_nltk_data()


def extract_keywords(text: str, max_keywords: int = 10) -> dict:
    """Extract keywords from text using RAKE.

    Args:
        text (str): Input text
        max_keywords (int, optional): Maximum number of keywords to return. Defaults to 10.

    Returns:
        dict: List of extracted keywords
    """
    if not text or not isinstance(text, str):
        return {'keywords': []}

    rake = Rake()
    rake.extract_keywords_from_text(text)
    keywords = rake.get_ranked_phrases()

    return {'keywords': keywords[:max_keywords]} 