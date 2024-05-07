import os

from cs50 import SQL
from flask import Flask, redirect, url_for, request, render_template, session
from flask_session import Session
from flask_mail import Mail, Message
from flask_socketio import SocketIO, join_room, leave_room, emit, send
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
import random


# Configure application
app = Flask(__name__)
app.secret_key = os.urandom(24)

socketio = SocketIO(app, cors_allowed_origins="http://localhost:5000")
if __name__ == '__main__':
    socketio.run(app, debug=True)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///chat.db")


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


# Configure mailing system
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'erichenrywisel@gmail.com'
app.config['MAIL_PASSWORD'] = 'jbuh ttxm ertp boip'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

# A dictionary containing rooms
active_rooms = {}


@app.route("/")
@login_required
def index():
    return render_template("index.html")

# Generates six digit


def generate_code():
    while True:
        code = ""
        for _ in range(6):
            code = str(random.randint(100000, 999999))

        if code not in active_rooms:
            break

    return code


@app.route("/register", methods=["GET", "POST"])
def register():
    # retrieve data form
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if username == "" or email == "" or password == "" or confirmation == "":
            return render_template("error.html", text="Field required")
        if password != confirmation:
            return render_template("error.html", text="Password doesn't match")
        if len(rows) == 1:
            return render_template("error.html", text="User already exists")
        if len(password) < 8 or len(password) > 12:
            return render_template("error.html", text="Password must be between 8-12 characters")

        # Inserts to database
        else:
            hash = generate_password_hash(password)
            session["user_id"] = db.execute("INSERT INTO users (username, hash, email) VALUES(?, ?, ?)", username, hash, email)
            return redirect("/")

    # if method is GET
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("error.html", text="Provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("error.html", text="Provide password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("error.html", text="User doesn't exist or incorrect password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


@app.route("/invite", methods=["GET", "POST"])
@login_required
def invite():
    if request.method == "POST":
        receiver = request.form.get("receiver")
        # Retrieve username from database
        data = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        sender = data[0]["username"]
        chat_code = generate_code()
        db.execute(
            "INSERT INTO invites (id, sender, chat_code, receiver) VALUES (?, ?, ?, ?)", session["user_id"], sender, chat_code, receiver)
        active_rooms[chat_code] = {"members": 0, "messages": []}

        # Send the invitation link to the receiver's email
        msg = Message('Invitation to join the chatroom', sender=("Purepost", "erichenrywisel@gmail.com"), recipients=[receiver])
        msg.body = f'Hi, it\'s {sender}! You are invited to join the chatroom on PurePost. Your Room Code is: {chat_code}'
        mail.send(msg)
        return redirect("/chatroom")
    else:
        return render_template("invite.html")

# Chat room to display message


@app.route("/chatroom")
@login_required
def chatroom():
    room = session.get("room")
    # if room is invalid return to index.html
    if room is None or room not in active_rooms:
        return redirect("/")

    return render_template("chatroom.html", roomcode=room, messages=active_rooms[room]["messages"])


@app.route("/join", methods=["GET", "POST"])
@login_required
def join():
    if request.method == "POST":
        name = request.form.get("name")
        roomcode = request.form.get("roomcode")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        # If any input is empty, display error
        if not name:
            return render_template("join.html", error="Please enter a name.", roomcode=roomcode, name=name)

        if join != False and not roomcode:
            return render_template("join.html", error="Please enter a room code.", roomcode=roomcode, name=name)

        room = roomcode
        if create != False:
            room = generate_code()
            active_rooms[room] = {"members": 0, "messages": []}

        elif roomcode not in active_rooms:
            return render_template("join.html", error="Invalid room code, or room doesn't exist", roomcode=roomcode, name=name)

        session["room"] = room
        session["name"] = name
        return redirect(url_for("chatroom"))
    else:
        return render_template("join.html")


@socketio.on("message")
def message(data):
    # to handle messages on client side
    room = session.get("room")
    name = session.get("name")
    if room not in active_rooms:
        return

    # contents
    content = {
        "name": name,
        "message": data["data"]
    }
    send(content, to=room)
    active_rooms[room]["messages"].append(content)
    print(f"{name} said: {data['data']}")


@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")
    if not room or not name:
        return
    if room not in active_rooms:
        leave_room(room)
        return

    join_room(room)
    send({"name": name, "message": "has entered the room"}, to=room)
    active_rooms[room]["members"] += 1
    print(f"{name} joined room")


@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    if room in active_rooms:
        active_rooms[room]["members"] -= 1
        if active_rooms[room]["members"] <= 0:
            del active_rooms[room]

    send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name} has left the room")


@app.route("/reset", methods=["GET", "POST"])
@login_required
def reset():
    if request.method == "GET":
        return render_template("reset.html")
    else:
        currentpassword = request.form.get("currentpassword")
        newpassword = request.form.get("newpassword")
        confirmation = request.form.get("confirmation")

        data = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        oldpassword = data[0]["hash"]
        if not check_password_hash(oldpassword, currentpassword):
            return render_template("error.html", text="Invalid Password")
        if currentpassword == "" or newpassword == "" or confirmation == "":
            return render_template("error.html", text="All fields are required")
        if newpassword != confirmation:
            return render_template("error.html", text="All fields are required")

        # Updates database with new password
        else:
            db.execute("UPDATE users SET hash = ? WHERE id = ?", generate_password_hash(newpassword), session["user_id"])
            return redirect("/")
