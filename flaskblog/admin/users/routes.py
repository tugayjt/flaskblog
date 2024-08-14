from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_bcrypt import Bcrypt
from flaskblog.common.utils import admin_required, handle_hashed_password_generate
from flaskblog.users.models import User
from flask_login import login_user, logout_user, current_user
from flaskblog.users.forms import LoginForm

users = Blueprint("users", __name__, url_prefix="/users")

bcrypt = Bcrypt()


@users.route("/", methods=["GET", "POST"])
@admin_required
def list_or_create_users():
        try:
            if request.method == "POST":
                name = request.form["username"]
                email = request.form["email"]
                password = handle_hashed_password_generate(request.form["password"])
                new_user = User(username=name, email=email, password=password)
                new_user.save_to_db()
                return redirect(url_for("users.list_or_create_users"))
        except Exception as e:
                return jsonify({"message": str(e)}),500
            
        users_list = User.query.all()
        return render_template("admin/users.html", users=users_list)
    


@users.route("/update/<int:user_id>", methods=["PUT"])
@admin_required
def update_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        if request.method == "PUT":
            user.username = request.form["username"]
            user.email = request.form["email"]
            user.update_db()
            return redirect(url_for("users.list_or_create_users"))
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    return render_template("admin/update_user.html", user=user)


@users.route("/delete/<int:user_id>", methods=["DELETE"])
@admin_required
def delete_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        user.delete_from_db()
        return jsonify({"message": "User was deleted successfully"})
    except Exception as e:
        return jsonify({"message": str(e)})


@users.route("/login", methods=["GET", "POST"])
@admin_required
def login():
    if current_user.is_authenticated and current_user.is_admin:
        return redirect(url_for("admin.users.list_or_create_users"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data, is_admin=True).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return (
                redirect(next_page)
                if next_page
                else redirect(url_for("admin.users.list_or_create_users"))
            )
        else:
            flash("Login Unsuccessful. Please check email and password", "danger")
    return render_template("admin/login.html", title="Login", form=form)


@users.route("/logout")
@admin_required
def logout():
    logout_user()
    return redirect(url_for("users.login"))