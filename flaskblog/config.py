from os import getenv
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
 
class Config:
    SECRET_KEY = getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI: str = getenv("SQLALCHEMY_DATABASE_URI")
    MAIL_SERVER: str = "smtp.googlemail.com"
    MAIL_PORT: int = 587
    MAIL_USE_TLS: bool = True
    MAIL_USERNAME: str = getenv("app_mail")
    MAIL_PASSWORD: str = getenv("app_pass")
    DEBUG = getenv("DEBUG") == "True"