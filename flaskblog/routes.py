from flask import render_template, url_for, flash, redirect, request, Response
from flaskblog import app, db
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post

with app.app_context():
    db.create_all()

posts = [
    {
        "author": "Corey Schafer",
        "title": "Blog post 1",
        "content": "First post content",
        "date_posted": "April 20, 2018",
    },
    {
        "author": "Jane Doe",
        "title": "Blog post 2",
        "content": "Second post content",
        "date_posted": "April 21, 2018",
    },
]


@app.route("/")
@app.route("/home")
def home() -> str:
    """
    Route for the home page.

    :return: Rendered HTML for the home page with blog posts.
    """
    return render_template("home.html", posts=posts, title="Home")


@app.route("/about")
def about() -> str:
    """
    Route for the about page.

    :return: Rendered HTML for the about page.
    """
    return render_template("about.html", title="About")


@app.route("/register", methods=["GET", "POST"])
def register() -> Response:
    """
    Route for the registration page.

    :return: Rendered HTML for the registration page or a redirect to the home page upon successful registration.
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for("home"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login() -> Response:
    """
    Route for the login page.

    :return: Rendered HTML for the login page or a redirect to the home page upon successful login.
    """
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "admin@blog.com" and form.password.data == "password":
            flash("You have been logged in!", "success")
            return redirect(url_for("home"))
        else:
            flash("Login Unsuccessful. Please check username and password", "danger")
    return render_template("login.html", title="Login", form=form)
