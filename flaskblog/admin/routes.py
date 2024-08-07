from flask import Blueprint, render_template, request, redirect, url_for, flash
from flaskblog import db
from flaskblog.users.models import User
from flaskblog.users.models import Post

admin = Blueprint('admin', __name__, url_prefix="/admin")

@admin.route("/users/", methods = ["GET","POST"])
def list_or_create_users():
    if request.method == 'POST':
        # Handle the creation of a new user
        name = request.form['name']
        email = request.form['email']
        new_user = User(name=name, email=email)
        new_user.save_to_db()
        return redirect(url_for('admin.list_or_create_users'))
    users = User.query.all()
    return render_template('admin/users.html', users=users)



@admin.route("/posts/", methods = ["GET","POST"])
def list_or_create_posts():
    if request.method == 'POST':
        # Handle the creation of a new user
        title = request.form['title']
        content = request.form['content']
        new_post = Post(title=title, content=content)
        new_post.save_to_db()
        return redirect(url_for('admin.list_or_create_posts'))
    posts = Post.query.all()
    return render_template('admin/posts.html', posts=posts)


@admin.route("/users/update/<int:user_id>",methods=["GET","PUT"])
def  update_user(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == "PUT":
        user.username = request.form["username"]
        user.email = request.form['email']
        user.save_to_db()
    return render_template("admin/users.html")


@admin.route("/users/delete/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    user.save_to_db()
    return render_template("admin/users.html")

