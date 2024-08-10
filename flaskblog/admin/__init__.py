from flask import Blueprint

admin = Blueprint('admin', __name__, url_prefix='/admin')

from flaskblog.admin.main.routes import main as main_blueprint
from flaskblog.admin.users.routes import users as users_blueprint
from flaskblog.admin.posts.routes import posts as posts_blueprint

admin.register_blueprint(main_blueprint)
admin.register_blueprint(users_blueprint)
admin.register_blueprint(posts_blueprint)
