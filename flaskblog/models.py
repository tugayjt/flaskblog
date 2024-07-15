from datetime import datetime
from flaskblog import db, app, login_manager
from flask_login import UserMixin


class ModelMixin:
    def save_to_db(self) -> None:
        """
        Save the current instance to the database.
        """
        with app.app_context():
            db.session.add(self)
            db.session.commit()


@login_manager.user_loader
def load_user(user_id: int) -> "User":
    """
    Load a user by ID.

    Args:
        user_id (int): The user ID.

    Returns:
        User: The user object.
    """
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """
    User model for storing user-related data.

    Attributes:
        id (int): The unique identifier for the user.
        username (str): The username of the user.
        email (str): The email address of the user.
        image_file (str): The filename of the user's profile image.
        password (str): The hashed password of the user.
        posts (List[Post]): The list of posts authored by the user.
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship("Post", backref="author", lazy=True)

    def __repr__(self) -> str:
        """
        Return a string representation of the user.

        Returns:
            str: The string representation of the user.
        """
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    """
    Post model for storing post-related data.

    Attributes:
        id (int): The unique identifier for the post.
        title (str): The title of the post.
        date_posted (datetime): The date and time the post was created.
        content (str): The content of the post.
        user_id (int): The ID of the user who authored the post.
    """

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self) -> str:
        """
        Return a string representation of the post.

        Returns:
            str: The string representation of the post.
        """
        return f"Post('{self.title}', '{self.date_posted}')"
