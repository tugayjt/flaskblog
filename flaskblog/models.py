from datetime import datetime
from itsdangerous import (
    BadSignature,
    SignatureExpired,
    URLSafeTimedSerializer as Serializer,
)
from flaskblog import db, login_manager, app
from flask_login import UserMixin
from typing import Union, Optional


class ModelMixin:
    def save_to_db(self) -> None:
        """
        Save the current instance to the database.
        """
        with app.app_context():
            db.session.add(self)
            db.session.commit()


@login_manager.user_loader
def load_user(user_id: int) -> Optional["User"]:
    """
    Load user by ID.

    Args:
        user_id (int): The ID of the user to load.

    Returns:
        Optional[User]: The user object if found, None otherwise.
    """
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(20), unique=True, nullable=False)
    email: str = db.Column(db.String(120), unique=True, nullable=False)
    image_file: str = db.Column(db.String(20), nullable=False, default="default.jpg")
    password: str = db.Column(db.String(60), nullable=False)
    posts = db.relationship("Post", backref="author", lazy=True)

    def get_reset_token(self, expires_sec: int = 1800) -> str:
        """
        Generates a time-limited token for password reset.

        Args:
            expires_sec (int, optional): Expiry time in seconds for the token (default is 1800).

        Returns:
            str: Generated reset token.
        """
        serializer = Serializer(app.config["SECRET_KEY"])
        return serializer.dumps(self.id, salt="reset-password")

    @staticmethod
    def verify_reset_token(token: str) -> Optional["User"]:
        """
        Verifies and retrieves user based on a provided reset token.

        Args:
            token (str): Reset token to verify.

        Returns:
            Optional[User]: User object if token is valid and not expired, None otherwise.
        """
        serializer = Serializer(app.config["SECRET_KEY"], salt="reset-password")
        try:
            user_id = serializer.loads(token, max_age=1800)
        except SignatureExpired:
            # Handle expired token (optional)
            return None
        except BadSignature:
            # Handle invalid token
            return None
        return User.query.get(user_id)

    def __repr__(self) -> str:
        """
        Returns a string representation of the User object.

        Returns:
            str: String representation of the User object.
        """
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    title: str = db.Column(db.String(100), nullable=False)
    date_posted: datetime = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
    content: str = db.Column(db.Text, nullable=False)
    user_id: int = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self) -> str:
        """
        Returns a string representation of the Post object.

        Returns:
            str: String representation of the Post object.
        """
        return f"Post('{self.title}', '{self.date_posted}')"
