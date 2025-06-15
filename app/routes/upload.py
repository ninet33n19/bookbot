import os
import uuid
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from app import db
from app.models.db import Document
from app.utils.file_check import allowed_file

bp = Blueprint('upload', __name__, url_prefix='/upload')

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@bp.route('/', methods=['POST'])
def upload_file():
    print("*** UPLOAD ROUTE HANDLER CALLED ***", flush=True)
    if 'file' not in request.files:
        return 'No file', 400

    uploaded_file = request.files['file']
    filename = uploaded_file.filename

    if not uploaded_file or not isinstance(filename, str) or not filename:
        return 'No selected file', 400

    file_id = str(uuid.uuid4())

    print(f"Processing file: {filename}")
    print(f"File allowed: {allowed_file(filename if filename is not None else '')}")

    if filename and allowed_file(filename if filename is not None else ''):
        safe_filename = secure_filename(filename)
        file_path = os.path.join(UPLOAD_FOLDER, file_id + "_" + safe_filename)
        uploaded_file.save(file_path)

        print(f"File saved to {file_path}")

        doc = Document()
        doc.id = file_id
        doc.filename = filename
        doc.path = file_path

        print(f"Document created with ID: {doc.id}")

        try:
            db.session.add(doc)
            db.session.commit()
            print(f"Database commit successful for ID: {doc.id}")
        except Exception as e:
            print(f"Database error: {str(e)}")
            db.session.rollback()
            return jsonify({'error': 'Database error'}), 500

        # Return the job_id
        return jsonify({
            'id': doc.id,
            'filename': doc.filename,
            'path': doc.path
        })
    else:
        print(f"File rejected: {filename}")
        return 'Invalid file type', 400
