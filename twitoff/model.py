""" SQLalchemy models and database management """

from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()

# Creates user table

class User(DB.Model):
    # id column is primary key for user table
    __tablename__ = 'user'

    id = DB.Column(DB.BigInteger, primary_key = True)
    username = DB.Column(DB.String, nullable = False)
    newest_tweet_id = DB.Column(DB.BigInteger)

    def __repr__(self):
        return f"<User: {self.username}>"      



# Created a tweets table

class Tweets(DB.Model):
    # id column is primary key for tweets table
    __table__ = 'tweets'

    id = DB.Column(DB.BigInteger, primary_key = True)
    text = DB.Column(DB.Unicode(300))
    vect = DB.Column(DB.PickleType, nullable = False)
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey(
        'user.id'), nullable = False)


    user = DB.relationship('User', backref = DB.backref('tweets', lazy = True))
    
    
 class Faves(DB.Model):
     id = DB.Column(DB.BigInteger, primary_key = True)
     text = DB.Column(DB.Unicode(300))
     user_id = DB.Column(DB.BigInterger, DB.ForeignKey(
         'user.id'), nullable = False
)   
    
    
    def __repr__(self):
        return f"<Tweet: {self.text}>"
