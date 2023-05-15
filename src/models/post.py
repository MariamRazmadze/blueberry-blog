from src.models.base import BaseModel
from src.extensions import db
from datetime import datetime
from slugify import slugify


class Post(BaseModel):

    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    excerpt = db.Column(db.String(200))
    image_name = db.Column(db.String(100))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    slug = db.Column(db.String(150), unique=True)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey(
        'author.id', ondelete='SET NULL'))
    author = db.relationship("Author", backref='posts')
    tags = db.relationship('Tag', secondary='post_tags', backref='posts')

    def generate_slug(self):
        self.slug = slugify(self.title)
