from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


with app.app_context():
    db.create_all()


posts = [
    {
        "author": "Corey Schafer",
        "title": "Blog Post 1",
        "content": "First post content",
        "date_posted": "April 20, 2018",
    },
    {
        "author": "Jane Doe",
        "title": "Blog Post 2",
        "content": "Second post content",
        "date_posted": "April 21, 2018",
    },
]


@app.route("/")
@app.route("/home")
def home() -> str:
    """
    Render the home page with posts.

    Returns:
        str: Rendered HTML template with posts.
    """
    return render_template("home.html", posts=posts)


@app.route("/about")
def about() -> str:
    """
    Render the about page.

    Returns:
        str: Rendered HTML template for the about page.
    """
    return render_template("about.html", title="About")


@app.route("/register", methods=["GET", "POST"])
def register() -> str:
    """
    Handle user registration.

    Returns:
        str: Rendered HTML template for registration page or redirects to login page upon successful registration.
    """
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            username=form.username.data, email=form.email.data, password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! You are now able to log in", "success")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login() -> str:
    """
    Handle user login.

    Returns:
        str: Rendered HTML template for login page or redirects to home page upon successful login.
    """
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Login Unsuccessful. Please check email and password", "danger")
    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
def logout() -> str:
    """
    Handle user logout.

    Returns:
        str: Redirects to home page after logging out.
    """
    logout_user()
    return redirect(url_for("home"))


@app.route("/account")
@login_required
def account() -> str:
    """
    Render the account page, requires login.

    Returns:
        str: Rendered HTML template for the account page.
    """
    return render_template("account.html", title="Account")
