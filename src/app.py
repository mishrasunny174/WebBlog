from flask import Flask, render_template, request, session, redirect

from src.models.blog import Blog
from src.models.user import User
from src.database.database import Database


app = Flask(__name__)
app.secret_key = 'Sexy Bitch'


@app.before_first_request
def initialize():
    Database.initialize()


@app.route('/')
def home():
    if session['email'] is not None:
        user = User.get_user_by_email(session['email'])
        blogs = user.get_blogs()
        return render_template("user_blogs.html", name=user.name, blogs=blogs)
    else:
        return render_template("index.html")


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/register')
def register():
    return render_template("register.html")


@app.route('/auth/login', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']

    if User.login_valid(email=email, password=password):
        User.login(user_email=email)
        user = User.get_user_by_email(session['email'])
        return render_template('user_blogs.html', name=user.name)
    else:
        session['email'] = None
        return 'ERROR: User Does not exist!'


@app.route('/auth/register', methods=['POST'])
def register_user():
    email = request.form['email']
    password = request.form['password']
    name = request.form['name']
    User.register(name=name, email=email, password=password)
    user = User.get_user_by_email(session['email'])
    return render_template('user_blogs.html', name=user.name)


@app.route('/blogs/<string:user_id>')
@app.route('/blogs/')
def list_blog(user_id=None):
    if user_id is not None:
        user = User.get_user_by_id(user_id)
    else:
        user = User.get_user_by_email(session['email'])
    blogs = user.get_blogs()
    return render_template('user_blogs.html', blogs=blogs, name=user.name)


@app.route('/posts/<string:blog_id>')
def list_post(blog_id):
    blog = Blog.from_mongo(blog_id)
    posts = blog.get_all_posts()
    return render_template('user_posts.html', posts=posts, name_of_blog=blog.title, blog_id=blog._id)


@app.route('/blogs/new', methods=['POST', 'GET'])
def create_new_blog():
    if request.method == 'GET':
        return render_template('new_blog.html')
    else:
        title = request.form['title']
        description = request.form['description']
        user = User.get_user_by_email(session['email'])
        user.new_blog(title, description)
        return redirect('/blogs/')


@app.route('/posts/new/<string:blog_id>', methods=['POST', 'GET'])
def create_new_post(blog_id):
    if request.method == 'GET':
        return render_template('new_post.html', blog_id=blog_id)
    else:
        title = request.form['title']
        content = request.form['content']
        user = User.get_user_by_email(session['email'])
        user.new_post(title=title, content=content, blog_id=blog_id)
        return redirect('/posts/'+blog_id)


@app.route('/auth/logout/')
def log_user_out():
    session['email'] = None
    return redirect('/')


@app.route('/blogs/search/', methods=['POST'])
def search_blogs_by_name():
    keyword = request.form['keyword']
    blogs = Blog.get_by_keyword(keyword=keyword)
    return render_template('list_blogs.html', blogs=blogs)


if __name__ == '__main__':
    app.run()
