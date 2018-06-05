from src.database.database import Database
from src.models.blog import Blog


Database.initialize()
blog = Blog(title='test2', author='test2', description='test2')

blog.save_to_mongo()

blogs = Blog.get_all_blogs()

for blog in blogs:
    print(blog.json())
