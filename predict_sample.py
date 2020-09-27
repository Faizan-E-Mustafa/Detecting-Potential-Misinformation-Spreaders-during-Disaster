from joblib import dump, load
import json
from collections import Counter

import numpy as np

from src import chi_square_filtering
from src import preprocessing


def predict_tweet(tweets):
    
    tweets = [preprocessing.preprocess(tweet) for tweet in tweets]
    #load models and classify
    pan_clf = load("./model/pan.joblib")
    ts = chi_square_filtering.Tweet_Selection()
    keep_words = ts.load_keep_words("./model/keep_words.pkl")
    
    tweets = ts.transform_for_predict([tweets], keep_words, keepn_tweets=30)
    tweets = tweets[0].tolist()
    pan_pred = pan_clf.predict([" ".join(tweets)])[0]
    
    disaster_clf = load("./model/disaster.joblib")
    predictions = np.array([disaster_clf.predict([tweet])[0] for tweet in tweets])
    disaster_tweets_indexes = np.where(predictions == 1)[0]
    disaster_counts = Counter(predictions)[1]
    
    # if more than 10 percent tweets are about disaster then label as disaster
    disaster_pred = 1 if disaster_counts / len(tweets) > 0.1 else 0

    if pan_pred and disaster_pred:
        print("potential misinformation spreader tweeting about disaster.")
    elif pan_pred or disaster_pred:
        if pan_pred:
            print("Potential misinformation spreader.")
        else:
            print("A regular user tweeting about disaster.")
    else:
        print("A regular user with routine tweet ")

    return pan_pred, disaster_pred, disaster_tweets_indexes


if __name__ == "__main__":

    with open("sample.json") as f:
        data = json.load(f)

    for user, tweets in data.items():

        print(f"\n####{user} prediction ####")
        pan_pred, disaster_pred, disaster_tweets_indexes = predict_tweet(tweets)
        print("\nTweets about Disaster :")

        for idx in disaster_tweets_indexes:
            print(f"- {tweets[idx]}")
