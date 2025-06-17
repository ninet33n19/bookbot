import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import os

# Ensure VADER lexicon is downloaded
def ensure_nltk_data():
    """Ensure required NLTK data is available"""
    try:
        nltk.data.find('vader_lexicon')
    except LookupError:
        nltk.download('vader_lexicon', quiet=True)

class SentimentAnalyzer:
    def __init__(self):
        ensure_nltk_data()
        self.analyzer = SentimentIntensityAnalyzer()
    
    def analyze_sentiment(self, text):
        """
        Analyze sentiment of given text using VADER sentiment analyzer
        
        Args:
            text (str): Text to analyze
            
        Returns:
            dict: Dictionary containing sentiment scores and classification
        """
        if not text or not isinstance(text, str):
            return {
                'compound': 0.0,
                'positive': 0.0,
                'negative': 0.0,
                'neutral': 0.0,
                'classification': 'neutral'
            }
        
        # Get sentiment scores
        scores = self.analyzer.polarity_scores(text)
        
        # Classify based on compound score
        if scores['compound'] >= 0.05:
            classification = 'positive'
        elif scores['compound'] <= -0.05:
            classification = 'negative'
        else:
            classification = 'neutral'
        
        return {
            'compound': round(scores['compound'], 3),
            'positive': round(scores['pos'], 3),
            'negative': round(scores['neg'], 3),
            'neutral': round(scores['neu'], 3),
            'classification': classification
        }
    
    def get_sentiment_summary(self, text):
        """
        Get a summary of sentiment analysis including additional metrics
        
        Args:
            text (str): Text to analyze
            
        Returns:
            dict: Comprehensive sentiment analysis results
        """
        sentiment = self.analyze_sentiment(text)
        
        # Calculate confidence level based on compound score
        confidence = abs(sentiment['compound'])
        if confidence >= 0.5:
            confidence_level = 'high'
        elif confidence >= 0.1:
            confidence_level = 'medium'
        else:
            confidence_level = 'low'
        
        return {
            'sentiment_scores': sentiment,
            'confidence_level': confidence_level,
            'confidence_score': round(confidence, 3)
        }

# Create a global instance
sentiment_analyzer = SentimentAnalyzer()
