from datetime import datetime
from flaskblog import db, app


class ModelMixin:
    def save_to_db(self) -> None:
        """
        Save the current instance to the database.
        """
        with app.app_context():
            db.session.add(self)
            db.session.commit()


class User(db.Model, ModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship("Post", backref="author", lazy=True)

    def __repr__(self) -> str:
        """
        Return a string representation of the User instance.

        :return: String representation of the User instance.
        """
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model, ModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self) -> str:
        """
        Return a string representation of the Post instance.

        :return: String representation of the Post instance.
        """
        return f"Post('{self.title}', '{self.date_posted}')"
