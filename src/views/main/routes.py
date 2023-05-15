from flask import Blueprint, render_template, abort
from flask_login import current_user, login_required
from src.utils import admin_required
from src.models.post import Post


main_blueprint = Blueprint("main", __name__, template_folder="templates")


def get_date(post):
    return post['date']


@main_blueprint.route("/")
def starting_page():
    latest_posts = Post.query.order_by(Post.date.desc()).limit(3).all()
    context = {
        "posts": latest_posts
    }
    return render_template("main/index.html", context=context)


@main_blueprint.route("/posts")
def posts():
    all_posts = Post.query.order_by(Post.date.desc()).all()
    context = {
        "all_posts": all_posts
    }
    return render_template("main/all-posts.html", context=context)


@main_blueprint.route("/posts/<slug>")
def post_detail(slug):
    identified_post = Post.query.filter_by(slug=slug).first()

    context = {
        "post": identified_post
    }

    if not identified_post:
        abort(404)

    return render_template("main/post-detail.html", context=context)
