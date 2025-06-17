from transformers import pipeline, Pipeline
from functools import lru_cache


@lru_cache(maxsize=1)
def _get_summarizer() -> Pipeline:
    """Load and cache the summarization model."""
    return pipeline('summarization', model='facebook/bart-large-cnn', tokenizer='facebook/bart-large-cnn', framework='pt', device_map='auto')


def generate_summary(text: str, max_length: int = 130, min_length: int = 30) -> dict:
    """Generate an abstractive summary of the input text.

    Args:
        text (str): Text to summarize
        max_length (int, optional): Maximum length of summary. Defaults to 130.
        min_length (int, optional): Minimum length of summary. Defaults to 30.

    Returns:
        dict: Dictionary containing the generated summary
    """
    if not text or not isinstance(text, str):
        return {'summary': ''}

    summarizer = _get_summarizer()
    # transformers pipeline returns a list of dicts with 'summary_text'
    summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)[0]['summary_text']

    return {'summary': summary} 