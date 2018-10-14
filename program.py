import program_tmembers
import program_tmakers
import data.mongo_setup as mongo_setup
from colorama import Fore
import infrastructure.state as state
import services.data_service as svc

from dateutil import parser


def main():
    mongo_setup.global_init()

    print_header()

    print(program_tmakers.create_account('leon', 'leon@gog.com', 'laddy'))
    # print(program_tmakers.logIntoAccount("ad@gog.com", "addy"))
    # program_tmakers.registerEvent(datetime.datetime.now(), 60, "Baseball2", "ad@gog.com")
    # try:
    #     while True:
    #         if find_user_intent() == 'book': #if the user wants to find an event
    #             program_tmembers.run()
    #         else:
    #             program_tmakers.run()  #if the user wants to create an event.
    # except KeyboardInterrupt:
    #     return


def print_header():
    sport = \
        """
            ~ SPORT COMPANION  ~
      Find a sportive person near you """

    print(Fore.WHITE + '****************  SPORT COMPANION  ****************')
    print(Fore.GREEN + sport)
    print(Fore.WHITE + '*********************************************')
    print()
    print("Welcome to Sport Companion!")
    print("What would you like to do?")
    print()


def find_user_intent():
    print("[m] Create a sport event at a place")
    print("[mem] Look for a sport events near your place")
    print()
    choice = input("Are you a team[m]aker or team [mem]ber ? ")
    if choice == 'm':
        return 'offer'

    return 'book'


from flask import Flask, render_template, request, redirect, url_for
import json
import flask_login
from flask_login import login_required

app = Flask(__name__)
login_manager = flask_login.LoginManager()
login_manager.login_view = "authenticate"
login_manager.login_message = u"Please log in to access this page."
app.secret_key = '123abcdefgfroothacks2018'  # Change this!


class User(flask_login.UserMixin):
    def __init__(self, email):
        self.id = email

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id


@login_manager.user_loader
def user_loader(email):
    # if email not in users.keys():
    #     return

    user = User(email)

    return user


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        passw = request.form["password"]
        login_id = request.form["email"]
        name = request.form["name"]
        print("REG", name, login_id, passw)
        program_tmakers.create_account(name, login_id, passw)
        return redirect(url_for("authenticate"))


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if state.active_account == None:
        return
    # if email not in users.keys():
    #     return
    print("EMAIL")
    print(email)
    user = User(email)
    user.id = email
    print("HERE 4")

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = True
    print("here 5")

    return user


success_response = json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route("/", methods=["GET"])
def home_page():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def authenticate():
    if request.method == "GET":
        return render_template("index.html")

    if request.method == "POST":
        passw = request.form["password"]
        login_id = request.form["email"]
        print(login_id, passw)
        auth_check = program_tmakers.checkAuth(login_id, passw)
        if auth_check:
            print("WE ARE HERE")
            user = User(login_id)
            user.id = login_id
            flask_login.login_user(user)
            print("WE GOT HERE2")
            return redirect(url_for('protected'))
        else:
            return render_template("index.html", error="Bad email and password pair")


@app.route('/home')
@login_required
def protected():
    print("IN PROTECTED")
    return render_template("main.html")


@app.route('/join', methods=["POST"])
@login_required
def join_event():
    event_id = request.form["event-id"]
    print("Curr", event_id)
    return success_response


@app.route("/events")
def all_activites():
    result = []
    for i in svc.getEvents():
        result.append({"id": str(i.id), "name": i.name, "time": str(i.startDate), "location": i.location})
    return json.dumps({'result': result})


@app.route('/create_event', methods=["POST"])
@login_required
def create_event():
    typpe = request.form['type']
    entry = parser.parse(request.form['date'])
    duration = float(request.form['duration'])
    location = request.form['location']
    idd = flask_login.current_user.id
    # Create Event in DB
    print("HELLOsasd")
    program_tmakers.registerEvent(entry, duration, typpe, idd, location)

    return success_response


@app.route('/preferences')
@login_required
def settings():
    return render_template("settings.html", userid=flask_login.current_user.id)


@app.route("/activities")
@login_required
def actvities():
    return render_template("activities.html")


@app.route("/update_prefs", methods=["POST"])
@login_required
def update_prefs():
    print("Hello")
    notif = request.form["notification-pref"]
    delay = request.form["delay"]
    print("Helloworld")
    print(notif, delay)
    print(flask_login.current_user.id)
    return render_template("settings.html", userid=flask_login.current_user.id)


@app.route('/logout')
@login_required
def logout():
    flask_login.logout_user()
    state.active_account = None

    return redirect(url_for('authenticate'))


if __name__ == '__main__':
    main()
    users = {'cl@cl.ca': {'password': 'cl@cl.ca'}}
    login_manager.init_app(app)
    app.run(debug=True)
