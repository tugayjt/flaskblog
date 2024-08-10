from flask import Blueprint, render_template, request, redirect, url_for
from flaskblog.common.utils import handle_hashed_password_generate, save_picture
from flaskblog.posts.routes import post
from flaskblog.users.models import User
from flaskblog.posts.models import Post
from flask_login import current_user

admin = Blueprint('admin', __name__, url_prefix="/admin")

@admin.route("/users/", methods=["GET", "POST"])
def list_or_create_users():
    if request.method == 'POST':
        name = request.form['username']
        email = request.form['email']
        password = handle_hashed_password_generate(request.form['password'])
        new_user = User(username=name, email=email, password=password)
        new_user.save_to_db()
        return redirect(url_for('admin.list_or_create_users'))
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@admin.route("/users/update/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    if request.method == "PUT":
        user = User.query.get_or_404(user_id)
        user.username = request.form["username"]
        user.email = request.form['email']
        user.update_db()
        return redirect(url_for('admin.list_or_create_users'))
    return render_template("admin/update_user.html")

@admin.route("/users/delete/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    user.delete_from_db()
    return redirect(url_for('admin.list_or_create_users'))

@admin.route("/posts/", methods=["GET", "POST"])
def list_or_create_posts():
    if request.method == 'POST':
        image = request.files.get("image")
        title = request.form["title"]
        short_desc = request.form['short_desc']
        content = request.form["content"]
        new_post = Post(title=title, content=content, short_desc=short_desc, author=current_user)
        if image:
            picture_file = save_picture(image,"posts/media")
            post.image_file = picture_file
        new_post.save_to_db()
        return redirect(url_for('admin.list_or_create_posts'))
    posts = Post.query.all()
    return render_template('admin/posts.html', posts=posts)

@admin.route("/posts/update/<int:post_id>", methods=["PUT"])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == "POST":
        post.title = request.form["title"]
        post.content = request.form['content']
        post.update_db()
        return redirect(url_for('admin.list_or_create_posts'))
    return render_template("admin/update_post.html")

@admin.route("/posts/delete/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.delete_from_db()
    return redirect(url_for('admin.list_or_create_posts'))
