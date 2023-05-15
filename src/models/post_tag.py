from src.models.base import BaseModel
from src.extensions import db


class PostTag(BaseModel):
    __tablename__ = "post_tags"

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
    tag_id = db.Column(db.Integer, db.ForeignKey("tag.id"))
