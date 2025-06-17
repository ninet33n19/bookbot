from flask import Blueprint, jsonify
from app.models.db import Document

bp = Blueprint('jobs', __name__, url_prefix='/jobs')

@bp.route('/<job_id>', methods=['GET'])
def job_status(job_id):
    doc = Document.query.get(job_id)
    if not doc:
        return jsonify({'error': 'Job not found'}), 404

    return jsonify({
        'status': doc.status,
        'result': doc.result
    })

