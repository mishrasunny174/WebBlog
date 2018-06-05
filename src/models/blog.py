from src.database.database import Database
from src.models.post import Post
import uuid
from datetime import datetime


class Blog(object):
    def __init__(self, title, author, description, date=datetime.utcnow(), _id=uuid.uuid4().hex):
        self.title = title
        self.author = author
        self.description = description
        self.date = date
        self._id = _id

    def json(self):
        return {'title': self.title,
                'author': self.author,
                'description': self.description,
                'date': self.date,
                '_id': self._id}

    def new_post(self, title, content, date, _id):
        post = Post(title=title, content=content, author=self.author, blog_id=self._id, date=date, _id=_id)
        post.save_to_mongo()

    def get_all_posts(self):
        return Post.get_posts_by_blog_id(self._id)

    def save_to_mongo(self):
        Database.insert(collection='blogs', data=self.json())

    @classmethod
    def from_mongo(cls, _id):
        blog_data = Database.find_one(collection='blogs', query={'_id': _id})
        return cls(**blog_data)

    @classmethod
    def get_all_blogs(cls):
        blogs = Database.find(collection='blogs', query={})
        return [cls(**blog) for blog in blogs]
