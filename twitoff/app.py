import os
import psycopg2 as pg2
from os import getenv
from flask import Flask, render_template, request
from .model import DB, User
from .twitter import add_or_update_user
from .predict import predict_user

def create_app():
    """ Creates and configures an instance of the Flask application """
    app = Flask(__name__)

    URI = os.getenv("DATABASE_URL")

    if URI.startswith("postgres://"):
        URI = URI.replace("postgres://", "postgresql://", 1)
    
    app.config["SQLALCHEMY_DATABASE_URI"] = URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    DB.init_app(app)
    
    conn = pg2.connect(URI, sslmode='require')


    @app.route('/')
    def root():
        
        users = User.query.all()
        return render_template("base.html", title = 'Home', users = users)

    @app.route('/compare', methods = ["POST"])
    def compare():
        user0, user1 = sorted(
            [request.values['user0'], request.values['user1']]
        )

        hypo_tweet_text = request.values["tweet_text"]

        if user0 == user1:
            message = "Cannot compare users to themselves!"

        else:
            prediction = predict_user(user0, user1, hypo_tweet_text)
            message = "{} is more likely than {} to have tweeted {}".format(
                user1 if prediction else user0,
                user0 if prediction else user1,
                hypo_tweet_text
                
            )

        return render_template('prediction.html', title = 'Prediction', message = message) 

    @app.route('/user', methods = ["POST"])
    @app.route('/user/<name>', methods = ["GET"])
    def user(name = None, message = ''):
        name = name or request.values["user_name"]
        try:
            if request.method == "POST":
                add_or_update_user(name)
                message = f"User {name} has been added to the database"

            tweets = User.query.filter(User.username == name).one().tweets
        
        except Exception as e:
            message = f"Error adding user {name} to database"
            tweets = []

        return render_template('user.html', title = name, tweets = tweets, message = message)       
        

   
    @app.route('/populate')
    def populate():
        add_or_update_user("elonmusk")
        add_or_update_user("jackblack")
        add_or_update_user("eigenrobot")
        return render_template("base.html", title = "Home", users = User.query.all())

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        users = User.query.all()
        return render_template("base.html", title = "Home", users = users)

    @app.route('/update')
    def update():
        for user in User.query.all():
            add_or_update_user(user.username)
        return render_template("base.html", title = "All user tweets updated!", users = User.query.all())
    
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

