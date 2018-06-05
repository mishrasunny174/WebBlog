from src.database.database import Database
from src.models.post import Post

Database.initialize()

post = Post(title='test1', content='test1', author='1234', blog_id='')

post.save_to_mongo()

posts = Post.from_mongo('test1')

for test_post in posts:
    print(test_post)