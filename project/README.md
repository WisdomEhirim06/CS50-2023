# PurePost
#### Video Demo:  <https://youtu.be/67h0KYMRlbA>
#### Description:

**PurePost** is a web chat that makes use of Flask, SocketIO and Javascript to make realtime connections.

In this Project, there are three major components:
* **templates**
* **app.py**
* **chat.db**

#### **templates**:
In templates there are nine different html pages, all having different functions.
However there is a base html page, where the other pages are just extensions of it.

Base.html contains an 'if' condition with jinja; If there's a session[id] then it displays a side navigation bar alongside index.html
Here's a look into what the navigation bar seems like:
* Chatroom (a disabled link)
* Invite a Friend (links to invite.html)
* Join (links to join.html)
* Reset (links to reset.html)
* Logout (logs user out)

But if there's no session then it displays:
* register.html
* login.html

The other templates include error.html for dynamically displaying error according to when certain conditions. Finally chatroom.html, the main focus of the application.
**chatroom.html** contains the client-side code. Javascript and SocketIO implementations are in chatroom.html.
Users can send and receive messages in realtime in chatroom.html.

register, login, invite, join, and reset all contain forms with POST methods, and actions (their respective app routings in Flask)

#### **chat.db**:
chat.db is a database containing two tables:
* **users**
     * id
     * username
     * password
     * email
* **invites**
      * id
      * sender's name
      * room id
      * receiver's email

Username can be retrieved from the database, as well as password updates and user authentication.

#### **app.py**:
app.py is the server side code for this web chat application. It contains app routings for the html pages and functions that handle messaging in chatrooms.


##### Configuration of app.py:

        import os

        from cs50 import SQL
        from flask import Flask, redirect, url_for, request, render_template, session
        from flask_session import Session
        from flask_mail import Mail, Message
        from flask_socketio import SocketIO, join_room, leave_room, emit
        from werkzeug.security import check_password_hash, generate_password_hash
        from functools import wraps
        import random

Above are the major functions and modules used in this application.
* cs50 provides SQL
* flask provides the necessary functions for app.py, which includes display of html pages and redirects
* flask_socketio provides functions for emitting messages, joining chatrooms, as well as leaving rooms.
* flask_session ensures that each user has a unique session.
* flask_mail provides functionalities to send invites to friends.
* werkzeug.security provides functionalities for hashing passwords and authentication
* random module helps in the generation of thr room code

##### To Configure application:

      app = Flask(__name__)
      app.secret_key = os.urandom(24)

      socketio = SocketIO(app)
      if __name__ == '__main__':
            socketio.run(app, debug=True)

##### To Configure session to use filesystem (instead of signed cookies):

      app.config["SESSION_PERMANENT"] = False
      app.config["SESSION_TYPE"] = "filesystem"
      Session(app)

##### To Configure cs50 library to use SQlite database:

      db = SQL("sqlite:///chat.db")

##### To Configure mailing system:

      app.config['MAIL_SERVER'] = 'smtp.gmail.com'
      app.config['MAIL_PORT'] = 465
      app.config['MAIL_USERNAME'] = 'erichenrywisel@gmail.com'
      app.config['MAIL_PASSWORD'] = 'jbuh ttxm ertp boip'
      app.config['MAIL_USE_TLS'] = False
      app.config['MAIL_USE_SSL'] = True

      mail = Mail(app)

**@app.route()**: This is a decorator in Flask used to create a route or endpoint.

#### Critical Choices Made:
* The first idea was to have tokens for the url of the chat rom.
* This would be the room's unique id.
* However, this was changed to using unique six digit codes.
* Join.html was the last update made, to ease access to the chatroom.

#### Errors encountered:
* Sending emails (invites to the chatroom) was difficult at first due to poor configuration of flask_mail
* Messages would not emit because emit was not imported from socketio
* Local host errors
* etc...

### How PurePost works
After successful **registration**, user is redirected to the home page.
At the home page, user has options to **send an invite**, **join a chatroom**, **reset password**, and even **log out**.

To join the chatroom, input your name and code, to join the room. If code is invalid, an error is emitted.
If the room code is valid, the user would be redirected to the chatroom.

To send invite, kindly input your friend's email, and an invite would be sent containing the **room code**.

You can also update your password ( with SQL's UPDATE, updating passwords would be easy.)

### Summary:

**Thank you CS50!!!.**

I learnt so much from this course. This project really made me realize how practical coding actually was.
I learnt the server-side of programming, a bit of javascript, flask and even frontend.

Once again, **thank you CS50!!!**
