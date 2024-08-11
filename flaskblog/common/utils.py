from flaskblog import bcrypt
import os
import secrets
from PIL import Image
from flask import current_app, redirect, flash, url_for
from flask_login import current_user
from functools import wraps


def handle_hashed_password_generate(entered_password):
    return bcrypt.generate_password_hash(entered_password).decode("utf-8")


def save_picture(form_picture, source) -> str:
    """
    Save a profile picture uploaded via a form.

    Args:
        form_picture (FileStorage): FileStorage object containing the picture to be saved.

    Returns:
        str: Filename of the saved picture.
    """
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, source, picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def admin_required(f):
    @wraps(f)
    
    def decorated_function(*args, **kwargs):
    
        if not current_user.is_authenticated:
            flash("You need to be logged in to access this page.", "warning")
            return redirect(url_for("users.login"))

        if not current_user.is_admin:
            flash("You don't have the required permissions.", "danger")
            return redirect(url_for("main.home"))

        return f(*args, **kwargs)

    return decorated_function