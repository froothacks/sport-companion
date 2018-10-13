from flask import Flask, render_template, request
import json
app = Flask(__name__)

success_response = json.dumps({'success':True}), 200, {'ContentType':'application/json'}


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
        return success_response
    else:
        return json.dumps({'success': False, 'data':auth_message}), 401, {'ContentType':'application/json'}


def check_user_creds(login, passw):
    message = "incorrect username and password combonation"
    if login == "cl@cl.ca" and passw == "abc":
        message = "" # Empty string for no error message
    return message



if __name__ == '__main__':
    app.run()
