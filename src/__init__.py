from flask import Flask
from src.config import Config
from src.views.main.routes import main_blueprint
from src.views.auth.routes import auth_blueprint
from src.extensions import db, migrate, login_manager, admin
from src.commands import init_db, populate_db
from src.models.base import BaseModel
from src.models.user import User
from src.models.author import Author
from src.models.post import Post
from src.models.tag import Tag
from src.models.post_tag import PostTag

from src.admin.models import UserModelView, AuthorModelView, PostModelView, TagModelView
from flask_admin.base import MenuLink

COMMANDS = [init_db, populate_db]
BLUEPRINTS = [main_blueprint, auth_blueprint]


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    register_blueprints(app)
    register_extensions(app)
    register_commands(app)

    return app


def register_blueprints(app):
    for blueprint in BLUEPRINTS:
        app.register_blueprint(blueprint)


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(_id):
        return User.query.get(_id)

    admin.init_app(app)
    admin.add_view(UserModelView(User, db.session))
    admin.add_view(AuthorModelView(Author, db.session))
    admin.add_view(PostModelView(Post, db.session))
    admin.add_view(TagModelView(Tag, db.session))
    admin.add_link(MenuLink("Go back", url="/",
                   icon_type="fa", icon_value="fa-sign-out"))


def register_commands(app):
    for command in COMMANDS:
        app.cli.add_command(command)
