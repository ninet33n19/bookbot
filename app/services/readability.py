import textstat

def get_readability_scores(text):
    """
    Calculate readability scores using Flesch-Kincaid and Gunning Fog indices.

    Args:
        text (str): The text to analyze

    Returns:
        dict: Dictionary containing Flesch-Kincaid and Gunning Fog scores
    """
    flesch_kincaid_score = textstat.flesch_kincaid_grade(text)
    gunning_fog_score = textstat.gunning_fog(text)

    return {
        'flesch_kincaid': flesch_kincaid_score,
        'gunning_fog': gunning_fog_score
    }
