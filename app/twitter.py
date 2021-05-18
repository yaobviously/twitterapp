from os import getenv
import tweepy
from .model import DB, Tweets, User
import tweepy
import spacy

# Authenticates our keys and enables us to use the Twitter API
API_KEY = getenv("TWITTER_KEY")
API_SECRET_KEY = getenv("TWITTER_SECRET_KEY")
TWITTER_AUTH = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
api = tweepy.API(TWITTER_AUTH)

# Loads the pickled spacy model
nlp = spacy.load("my_model")


# A function to vectorize tweets
def vectorize_tweet(tweet_text):
    return nlp(tweet_text).vector


# Updating or adding users and their tweets   
def add_or_update_user(username):
    """ 
    Adds a Twitter User and their 200 most recent tweets to our db    
    """

    try:
        twitter_user = api.get_user(user)        
        
        db_user = User.query.get(twitter_user.id) or User(
            id = twitter_user.id, username = username)
        
        
        DB.session.add(db_user)

        tweets = twitter_user.timeline(
            count = 200,
            exclude_replies = True,
            include_rts = False,
            tweet_mode = 'extended',
            since_id = db_user.newest_tweet_id
        )

        if tweets:
            db_user.newest_tweet_id = tweets[0].id

        for tweet in tweets:
            tweet_vector = vectorize_tweet(tweet.full_text)

            db_tweet = Tweet(
                id = tweet.id, text = tweet.full_text, vect = tweet_vector
            )

            db_user.tweets.append(db_tweet)

            DB.session.add(db_tweet)

    except Exception as e:
        print(f'Error Processing {username}: {e}')
        raise e

    else:
        DB.session.commit()

