""" Handles DS Prediction Model """
from .twitter import vectorize_tweet
import numpy as np
from .model import User
from sklearn.linear_model import LogisticRegression
# user0 = 'elonmusk'
# user1 = 'JackBlack'

log_reg = LogisticRegression()

def predict_user(user0_name, user1_name, hypo_text):
    """ Which user is more likely to have tweeted a tweet?

    Returns 0 for user0_name and 1 for user1_name
    
     """

    user0 = User.query.filter(User.username == user0_name).one()
    user1 = User.query.filter(User.username == user1_name).one()

    user0_vectors = np.array([tweet.vect for tweet in user0.tweets])
    user1_vectors = np.array([tweet.vect for tweet in user1.tweets])

    vectors = np.vstack([user0_vectors, user1_vectors])

    labels = np.concatenate(
        [np.zeros(len(user0.tweets)), np.ones(len(user1.tweets))])

    log_reg = LogisticRegression().fit(vectors, labels)

    hypo_tweet_vect = vectorize_tweet(hypo_text).reshape(1,-1)

    return log_reg.predict(hypo_tweet_vect)

    
    user_test = User.query.filter(User.username == "elonmusk").one()
    print(user_test)