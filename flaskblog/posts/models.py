from flaskblog.common.mixins import ModelMixin
from flaskblog import db
from datetime import datetime

class Post(db.Model, ModelMixin):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    short_desc = db.Column(db.String(100))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Change to datetime.utcnow
    content = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(20), default="default.jpg")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
