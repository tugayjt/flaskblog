from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Create the Flask application instance
app: Flask = Flask(__name__)

# Configure the Flask application
app.config["SECRET_KEY"] = "5791628bb0b13ce0c676dfde280ba245"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

# Initialize extensions
db: SQLAlchemy = SQLAlchemy(app)
bcrypt: Bcrypt = Bcrypt(app)
login_manager: LoginManager = LoginManager(app)

# Configure the LoginManager
login_manager.login_view = "login"
login_manager.login_message_category = "info"

# Import routes
import flaskblog.routes


def create_app() -> Flask:
    """
    Create and configure the Flask application.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "5791628bb0b13ce0c676dfde280ba245"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Import and register routes
    with app.app_context():
        import flaskblog.routes

    return app


if __name__ == "__main__":
    app.run(debug=True)
