from flask import Flask, render_template, request, session
from src.models.user import User
from src.database.database import Database


app = Flask(__name__)
app.secret_key = 'Sexy Bitch'


@app.before_first_request
def initialize():
    Database.initialize()


@app.route('/login')
def start_method():
    return render_template("login.html")


@app.route('/register')
def start_method():
    return render_template("register.html")


@app.route('/auth/login', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']

    if User.login_valid(email=email, password=password):
        User.login(user_email=email)
        return render_template('profile.html', email=session['email'])
    else:
        session['email'] = None
        return 'ERROR: User Does not exist!'


@app.route('/auth/register', methods=['POST'])
def register_user():
    email = request.form['email']
    password = request.form['password']
    User.register(email=email, password=password)
    return render_template('profile.html', email=session['email'])


if __name__ == '__main__':
    app.run()
