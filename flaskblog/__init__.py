import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Initialize Flask application
app: Flask = Flask(__name__)

# Set secret key for the Flask application
app.config["SECRET_KEY"] = "5791628bb0b13ce0c676dfde280ba245"

# Configure SQLAlchemy with SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

# Initialize SQLAlchemy
db: SQLAlchemy = SQLAlchemy(app)

# Initialize Bcrypt for password hashing
bcrypt: Bcrypt = Bcrypt(app)

# Initialize LoginManager for managing user sessions
login_manager: LoginManager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

# Configure Flask-Mail with Gmail's SMTP server
app.config["MAIL_SERVER"] = "smtp.googlemail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("app_mail")
app.config["MAIL_PASSWORD"] = os.getenv("app_pass")

# Initialize Mail
mail: Mail = Mail(app)

# Import routes from the flaskblog package
from flaskblog import routes
