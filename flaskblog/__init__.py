from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app)

from flaskblog import routes


def create_app() -> Flask:
    """
    Factory function to create and configure the Flask application.

    :return: Configured Flask application.
    """
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "secret"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app


app = create_app()
