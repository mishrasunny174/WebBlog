from src.database.database import Database
from src.models.post import Post

Database.initialize()

#post = Post(title='test1', content='test1', author='1234', blog_id='')

#post.save_to_mongo()

posts = Post.get_posts_by_blog_id('test1')

for test_post in posts:
    print(test_post)