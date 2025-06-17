from app import create_app, db
from app.models.db import Document
from celery import Celery
from app.core.config import Config
from app.services.sentiment_analysis import sentiment_analyzer
import textstat
from app.services.sentence_complexity import analyze_sentence_complexity
from app.services.lexical_diversity import analyze_lexical_diversity
from app.services.named_entity_recognition import analyze_named_entities
from app.services.keyword_extraction import extract_keywords
from app.services.auto_summarization import generate_summary

celery = Celery(
    'wordlens',
    broker=Config.CELERY_BROKER_URL,
    backend=Config.CELERY_RESULT_BACKEND
)

celery.conf.task_routes = {
    'app.workers.celery_workers.text_analysis_service': {'queue': 'celery'},
    'app.workers.celery_workers.readability_service': {'queue': 'celery'},  # backward compatibility
    'app.workers.celery_workers.sentence_complexity_service': {'queue': 'celery'},
    'app.workers.celery_workers.lexical_diversity_service': {'queue': 'celery'},
    'app.workers.celery_workers.ner_service': {'queue': 'celery'},
    'app.workers.celery_workers.keyword_extraction_service': {'queue': 'celery'},
    'app.workers.celery_workers.auto_summarization_service': {'queue': 'celery'},
}

def calculate_readability_metrics(text):
    """Calculate comprehensive readability metrics for the text"""
    try:
        word_count = len(text.split())
        sentence_count = textstat.sentence_count(text)
        
        readability_metrics = {
            'word_count': word_count,
            'sentence_count': sentence_count,
            'character_count': len(text),
            'avg_words_per_sentence': round(word_count / max(sentence_count, 1), 2),
            'flesch_reading_ease': round(textstat.flesch_reading_ease(text), 2),
            'flesch_kincaid_grade': round(textstat.flesch_kincaid_grade(text), 2),
            'gunning_fog': round(textstat.gunning_fog(text), 2),
            'automated_readability_index': round(textstat.automated_readability_index(text), 2),
            'coleman_liau_index': round(textstat.coleman_liau_index(text), 2),
            'linsear_write_formula': round(textstat.linsear_write_formula(text), 2),
            'dale_chall_readability_score': round(textstat.dale_chall_readability_score(text), 2)
        }
        
        # Add reading level interpretation
        flesch_score = readability_metrics['flesch_reading_ease']
        if flesch_score >= 90:
            reading_level = 'Very Easy'
        elif flesch_score >= 80:
            reading_level = 'Easy'
        elif flesch_score >= 70:
            reading_level = 'Fairly Easy'
        elif flesch_score >= 60:
            reading_level = 'Standard'
        elif flesch_score >= 50:
            reading_level = 'Fairly Difficult'
        elif flesch_score >= 30:
            reading_level = 'Difficult'
        else:
            reading_level = 'Very Difficult'
        
        readability_metrics['reading_level'] = reading_level
        
        return readability_metrics
    except Exception as e:
        return {'error': f'Error calculating readability metrics: {str(e)}'}

@celery.task(name='app.workers.celery_workers.text_analysis_service')
def text_analysis_service(file_id):
    """
    Combined task that performs both readability analysis and sentiment analysis
    """
    # Create a new app context for this task
    flask_app = create_app()
    with flask_app.app_context():
        doc = Document.query.get(file_id)
        print(f"Processing document with ID: {doc.id}")
        
        try:
            # Read the file content
            with open(doc.path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            if not text.strip():
                doc.status = 'FAILED'
                doc.result = {'error': 'File is empty or could not be read'}
                db.session.commit()
                return
            
            # Perform readability analysis
            readability_results = calculate_readability_metrics(text)
            
            # Perform sentiment analysis
            sentiment_results = sentiment_analyzer.get_sentiment_summary(text)
            
            # Perform sentence complexity analysis
            complexity_results = analyze_sentence_complexity(text)
            
            # Perform lexical diversity analysis
            lexical_results = analyze_lexical_diversity(text)
            
            # Perform NER analysis
            ner_results = analyze_named_entities(text)
            
            # Perform keyword extraction
            keyword_results = extract_keywords(text)
            
            # Perform auto summarization (lightweight default limits)
            summary_results = generate_summary(text)
            
            # Combine results
            analysis_results = {
                'readability_analysis': readability_results,
                'sentence_complexity': complexity_results,
                'lexical_diversity': lexical_results,
                'named_entity_recognition': ner_results,
                'keyword_extraction': keyword_results,
                'sentiment_analysis': sentiment_results,
                'auto_summarization': summary_results,
                'text_preview': text[:200] + '...' if len(text) > 200 else text,
                'analysis_timestamp': None  # Will be set by the database
            }
            
            doc.status = 'COMPLETED'
            doc.result = analysis_results
            
        except FileNotFoundError:
            doc.status = 'FAILED'
            doc.result = {'error': 'File not found'}
        except UnicodeDecodeError:
            doc.status = 'FAILED'
            doc.result = {'error': 'File encoding not supported. Please use UTF-8 encoded text files.'}
        except Exception as e:
            doc.status = 'FAILED'
            doc.result = {'error': f'Unexpected error during analysis: {str(e)}'}
        
        db.session.commit()
        print(f"Document {doc.id} analysis completed with status: {doc.status}")

# Keep the old task name for backward compatibility, but redirect to new service
@celery.task(name='app.workers.celery_workers.readability_service')
def readability_service(file_id):
    """Legacy task - redirects to the new comprehensive text analysis service"""
    return text_analysis_service(file_id)

# -------------------  INDIVIDUAL SERVICE TASKS  ------------------- #


def _load_document(file_id):
    """Utility to load document by ID inside an app context."""
    flask_app = create_app()
    with flask_app.app_context():
        return Document.query.get(file_id), flask_app


@celery.task(name='app.workers.celery_workers.sentence_complexity_service')
def sentence_complexity_service(file_id):
    doc, app_ctx = _load_document(file_id)
    with app_ctx.app_context():
        try:
            with open(doc.path, 'r', encoding='utf-8') as f:
                text = f.read()
            doc.result = analyze_sentence_complexity(text)
            doc.status = 'COMPLETED'
        except Exception as e:
            doc.status = 'FAILED'
            doc.result = {'error': str(e)}
        db.session.commit()


@celery.task(name='app.workers.celery_workers.lexical_diversity_service')
def lexical_diversity_service(file_id):
    doc, app_ctx = _load_document(file_id)
    with app_ctx.app_context():
        try:
            with open(doc.path, 'r', encoding='utf-8') as f:
                text = f.read()
            doc.result = analyze_lexical_diversity(text)
            doc.status = 'COMPLETED'
        except Exception as e:
            doc.status = 'FAILED'
            doc.result = {'error': str(e)}
        db.session.commit()


@celery.task(name='app.workers.celery_workers.ner_service')
def ner_service(file_id):
    doc, app_ctx = _load_document(file_id)
    with app_ctx.app_context():
        try:
            with open(doc.path, 'r', encoding='utf-8') as f:
                text = f.read()
            doc.result = analyze_named_entities(text)
            doc.status = 'COMPLETED'
        except Exception as e:
            doc.status = 'FAILED'
            doc.result = {'error': str(e)}
        db.session.commit()


@celery.task(name='app.workers.celery_workers.keyword_extraction_service')
def keyword_extraction_service(file_id):
    doc, app_ctx = _load_document(file_id)
    with app_ctx.app_context():
        try:
            with open(doc.path, 'r', encoding='utf-8') as f:
                text = f.read()
            doc.result = extract_keywords(text)
            doc.status = 'COMPLETED'
        except Exception as e:
            doc.status = 'FAILED'
            doc.result = {'error': str(e)}
        db.session.commit()


@celery.task(name='app.workers.celery_workers.auto_summarization_service')
def auto_summarization_service(file_id):
    doc, app_ctx = _load_document(file_id)
    with app_ctx.app_context():
        try:
            with open(doc.path, 'r', encoding='utf-8') as f:
                text = f.read()
            doc.result = generate_summary(text)
            doc.status = 'COMPLETED'
        except Exception as e:
            doc.status = 'FAILED'
            doc.result = {'error': str(e)}
        db.session.commit()
