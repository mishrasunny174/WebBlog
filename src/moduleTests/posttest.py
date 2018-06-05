from src.database.database import Database
from src.models.post import Post

Database.initialize()

post = Post(title='test1', content='test1', author='test1', blog_id='1234')

post.save_to_mongo()

posts = Post.get_posts_by_blog_id('1234')

for test_post in posts:
    print(test_post.json())
