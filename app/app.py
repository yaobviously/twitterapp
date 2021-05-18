from os import getenv
from flask import Flask, render_template
from .model import DB, User
from .twitter import add_or_update_user

def create_app():
    """ Creates and configures an instance of the Flask application """
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///twitter.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    DB.init_app(app)

    @app.route('/')
    def root():
        users = User.query.all()
        return render_template("base.html", title = 'Home', users = users)
   
   
    @app.route('/populate')
    def populate():
        add_or_update_user("elonmusk")
        add_or_update_user("jackblack")
        return render_template("base.html", title = "Home", users = Users.query.all())

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        users = User.query.all()
        return render_template("base.html", title = "Home", users = users)        

    return app


# def insert_users(usernames):
#     for id_index, username in enumerate(usernames):
#         user = User(id = id_index, username = username)
#         DB.session.add(user)
#         DB.session.commit()


# def insert_tweet(user_id, text):
#     tweet = Tweets(user_id = user_id, text = str(text))
#     DB.session.add(tweet)
#     DB.session.commit()

