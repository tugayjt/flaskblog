from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User


class RegistrationForm(FlaskForm):
    """
    Form for user registration.

    Attributes:
        username (StringField): Username field.
        email (StringField): Email field.
        password (PasswordField): Password field.
        confirm_password (PasswordField): Password confirmation field.
        submit (SubmitField): Submit button.
    """

    username: StringField
    email: StringField
    password: PasswordField
    confirm_password: PasswordField
    submit: SubmitField

    def validate_username(self, username: StringField):
        """
        Validate if the username is already taken.

        Args:
            username (StringField): Username to validate.

        Raises:
            ValidationError: If the username is already taken.
        """
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "That username is taken. Please choose a different one."
            )

    def validate_email(self, email: StringField):
        """
        Validate if the email address is already taken.

        Args:
            email (StringField): Email address to validate.

        Raises:
            ValidationError: If the email address is already taken.
        """
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("That email is taken. Please choose a different one.")


class LoginForm(FlaskForm):
    """
    Form for user login.

    Attributes:
        email (StringField): Email field.
        password (PasswordField): Password field.
        remember (BooleanField): Checkbox to remember user session.
        submit (SubmitField): Submit button.
    """

    email: StringField
    password: PasswordField
    remember: BooleanField
    submit: SubmitField


class UpdateAccountForm(FlaskForm):
    """
    Form for updating user account details.

    Attributes:
        username (StringField): Username field.
        email (StringField): Email field.
        picture (FileField): Field for updating profile picture.
        submit (SubmitField): Submit button.
    """

    username: StringField
    email: StringField
    picture: FileField
    submit: SubmitField

    def validate_username(self, username: StringField):
        """
        Validate if the new username is already taken.

        Args:
            username (StringField): New username to validate.

        Raises:
            ValidationError: If the new username is already taken.
        """
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    "That username is taken. Please choose a different one."
                )

    def validate_email(self, email: StringField):
        """
        Validate if the new email address is already taken.

        Args:
            email (StringField): New email address to validate.

        Raises:
            ValidationError: If the new email address is already taken.
        """
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    "That email is taken. Please choose a different one."
                )
