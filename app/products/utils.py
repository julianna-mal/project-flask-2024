import os
import uuid
from flask import current_app
from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}


def save_product_image(file):
    if not file or not file.filename:
        return None

    filename = secure_filename(file.filename)

    if "." not in filename:
        return None

    extension = filename.rsplit(".", 1)[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        return None

    new_filename = f"{uuid.uuid4().hex}.{extension}"

    upload_folder = os.path.join(
        current_app.root_path,
        "products",
        "static",
        "uploads"
    )

    os.makedirs(upload_folder, exist_ok=True)

    file.save(os.path.join(upload_folder, new_filename))

    return f"uploads/{new_filename}"