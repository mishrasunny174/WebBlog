from src.database.database import Database
from datetime import datetime
import uuid


class Post(object):
    def __init__(self, title, content, author, blog_id, date=datetime.utcnow(), _id=uuid.uuid4().hex()):
        self.title = title
        self.content = content
        self.author = author
        self._id = _id
        self.blog_id = blog_id
        self.date = date

    def json(self):
        return {'title': self.title,
                'content': self.content,
                'author': self.author,
                'blog_id': self.blog_id,
                'date': self.date,
                '_id': self._id}

    def save_to_mongo(self):
        Database.insert(collection='posts', data=self.json())

    @classmethod
    def from_mongo(cls, _id):
        post_data = Database.find(collection='posts', query={'_id': _id})
        return cls(**post_data)

    @classmethod
    def get_posts_by_blog_id(cls, blog_id):
        return [post for post in Database.find(collection='posts', query={'blog_id': blog_id})]
