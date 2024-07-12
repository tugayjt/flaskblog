from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    """
    Form for user registration.

    Attributes:
        username (StringField): The user's username.
        email (StringField): The user's email address.
        password (PasswordField): The user's password.
        confirm_password (PasswordField): Confirmation of the user's password.
        submit (SubmitField): The submit button for the form.
    """

    username: StringField = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    email: StringField = StringField("Email", validators=[DataRequired(), Email()])
    password: PasswordField = PasswordField("Password", validators=[DataRequired()])
    confirm_password: PasswordField = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit: SubmitField = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    """
    Form for user login.

    Attributes:
        email (StringField): The user's email address.
        password (PasswordField): The user's password.
        remember (BooleanField): Checkbox to remember the user.
        submit (SubmitField): The submit button for the form.
    """

    email: StringField = StringField("Email", validators=[DataRequired(), Email()])
    password: PasswordField = PasswordField("Password", validators=[DataRequired()])
    remember: BooleanField = BooleanField("Remember Me")
    submit: SubmitField = SubmitField("Login")
