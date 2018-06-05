from datetime import datetime

from flask import session

from src.database.database import Database
import uuid

from src.models.blog import Blog


class User(object):
    def __init__(self, name, email, password, _id=uuid.uuid4().hex):
        self.name = name
        self.email = email
        self.password = password
        self._id = _id

    @classmethod
    def get_user_by_email(cls, email):
        data = Database.find_one(collection='users', query={'email': email})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_user_by_id(cls, _id):
        data = Database.find_one(collection='users', query={'_id': _id})
        if data is not None:
            return cls(**data)

    @staticmethod
    def login_valid(email, password):
        user = User.get_user_by_email(email)
        if user is not None:
            # user is found with passed email, check password
            return user.password == password
        return False  # return false if user doesn't exist with passed email

    @classmethod
    def register(cls, email, password):
        user = cls.get_user_by_email(email)
        if user is None:
            # user doesn't exist we can create a new user with this email
            new_user = cls(email=email, password=password)
            new_user.save_to_mongo()
            session['email'] = email
            return True
        else:
            # user does exist with this passed email can't create a new one
            return False

    @staticmethod
    def login(user_email):
        session['email'] = user_email

    @staticmethod
    def logout():
        session['email'] = None

    def get_blogs(self):
        return Blog.blogs_by_author_id(self._id)

    def new_blog(self, title, description):
        blog = Blog(title=title, author=self.name, description=description, author_id=self._id)
        blog.save_to_mongo()

    @staticmethod
    def new_post(blog_id, title, content, date=datetime.utcnow()):
        blog = Blog.from_mongo(blog_id)
        blog.new_post(title=title, content=content, date=date)

    def json(self):
        return {'name': self.name,
                'email': self.email,
                'password': self.password,
                '_id': self._id}

    def save_to_mongo(self):
        Database.insert(collection='users', data=self.json())