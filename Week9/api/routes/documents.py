import logging
import os
import tempfile

from flask import Blueprint, g, jsonify, request
from scripts.db_utils import store_document_vectors
from scripts.embedding_service import EmbeddingService
from werkzeug.utils import secure_filename

from api.db import db
from api.decorators import jwt_required
from api.models import Document

documents_bp = Blueprint("documents", __name__, url_prefix="/documents")

ALLOWED_EXTENSIONS = {"txt"}
logger = logging.getLogger(__name__)


def allowed_file(filename: str) -> bool:
    """Check if a file is allowed to be uploaded based on its extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@documents_bp.route("/upload", methods=["POST"])
@jwt_required
def upload_document():
    """
    Upload a text file, save metadata to DB, chunk content,
    generate embeddings, and store in pgvector tagged with user_id.
    """
    # Debug info (remove in production)
    print(">>> Content-Type:", request.content_type)
    print(">>> request.files keys:", list(request.files.keys()))
    print(">>> request.form keys:", list(request.form.keys()))

    if "file" not in request.files:
        return (
            jsonify(
                {
                    "error": "No file part in request. "
                    "Please send form-data with key 'file' and attach a .txt file."
                }
            ),
            400,
        )

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Only .txt files are allowed"}), 400

    filename = secure_filename(file.filename)

    # Save file temporarily
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        file.save(tmp.name)
        tmp_path = tmp.name

    try:
        # Read file content
        with open(tmp_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Save metadata in DB
        document = Document(
            filename=filename,
            owner_id=getattr(g.current_user, "id", g.current_user.get("id")),
            visibility="user",
            content_type="text/plain",
            size=len(content.encode("utf-8")),
        )
        db.session.add(document)
        db.session.commit()

        # Generate embeddings
        embeddings = EmbeddingService.get_huggingface_embeddings()
        store_document_vectors(
            user_id=document.owner_id,
            document_id=document.id,
            content=content,
            embedding_instance=embeddings,
        )

        return (
            jsonify(
                {
                    "message": "Document uploaded successfully",
                    "document": document.serialize(),
                }
            ),
            201,
        )

    except Exception as e:
        db.session.rollback()
        logger.exception(f"Failed to process document upload: {e}")
        return jsonify({"error": f"Failed to process document: {str(e)}"}), 500

    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
