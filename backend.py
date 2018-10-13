from flask import Flask, render_template, request, redirect, url_for
import json
import flask_login
from flask_login import login_required

app = Flask(__name__)
login_manager = flask_login.LoginManager()
app.secret_key = '123abcdefgfroothacks2018'  # Change this!


class User(flask_login.UserMixin):
    def __init__(self):
        id = None

    def is_authenticated(self):
        return self.is_authenticated

    def get_id(self):
        return 123


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['password'] == users[email]['password']

    return user


success_response = json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route("/", methods=["GET"])
def home_page():
    return render_template("index.html")


@app.route("/loginedin", methods=["GET"])
def user_dash():
    return render_template("main.html")


@app.route("/auth", methods=["POST"])
def authenticate():
    passw = request.form["password"]
    login_id = request.form["email"]
    print(login_id, passw)
    auth_message = check_user_creds(login_id, passw)
    print(auth_message)
    if auth_message == "":
        user = User()
        user.id = login_id
        flask_login.login_user(user)
        return redirect(url_for('/protected'))

    else:
        return auth_message


@app.route('/protected')
@login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id


def check_user_creds(login, passw):
    message = "incorrect username and password combonation"
    if login == "cl@cl.ca" and passw == "cl@cl.ca":
        message = ""  # Empty string for no error message
    return message


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'


if __name__ == '__main__':
    users = {'cl@cl.ca': {'password': 'cl@cl.ca'}}
    login_manager.init_app(app)
    app.run()
