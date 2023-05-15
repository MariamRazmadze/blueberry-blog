from flask.cli import with_appcontext
from src.extensions import db
from src.models.user import User, UserRole, Role
from src.models.author import Author
from src.models.post import Post
import click


@click.command("init_db")
@with_appcontext
def init_db():
    click.echo("Creating Database")
    db.drop_all()
    db.create_all()
    click.echo("Finished Creating Database")


@click.command("populate_db")
@with_appcontext
def populate_db():
    click.echo("Creating users")
    admin_user = User(email="admin@mail.com",
                      username="testuser1", password="password123")
    admin_user.create()

    roles = ["user", "moderator", "admin"]
    for role in roles:
        new_role = Role(name=role)
        new_role.create()

    admin_role = Role.query.filter_by(name="admin").first()
    admin_user_role = UserRole(user_id=admin_user.id, role_id=admin_role.id)
    admin_user_role.create()
    click.echo("Finished Creating Database")
