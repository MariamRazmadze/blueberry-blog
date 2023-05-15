from src.models.base import BaseModel
from src.extensions import db


class Tag(BaseModel):
    __tablename__ = "tag"

    id = db.Column(db.Integer, primary_key=True)
    caption = db.Column(db.String(20))

    def __str__(self):
        return self.caption
