import pickle
import pandas as pd
import numpy as np
from tqdm import tqdm

from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.feature_extraction.text import TfidfVectorizer


class Tweet_Selection:
    """Filter most important tweets using chi-square"""

    def fit(self, df_train, nimportant_words=4000):
        """get list of important words (keep_words)"""

        self.keep_words = self.get_n_important_words(df_train, N=nimportant_words)

    def get_n_important_words(self, df_train, N):

        vectorizer = TfidfVectorizer(sublinear_tf=True)
        X_train = vectorizer.fit_transform(
            [" ".join(user_tweets) for user_tweets in df_train.tweets]
        )

        feature_names = vectorizer.get_feature_names()
        ch2 = SelectKBest(chi2, k=N)
        X_train = ch2.fit_transform(X_train, df_train.target)

        keep_words = np.array(feature_names)[ch2.get_support(indices=True)]
        return keep_words

    def transform(self, df, keepn_tweets=30):
        """keep top n tweets in which important words occurs most frequently"""

        selected_tweets, scores = self.select_topn_tweets(
            df.tweets, self.keep_words, keep_topn=keepn_tweets
        )

        df["TopN_Tweets"] = selected_tweets
        df["Tweet_Scores"] = scores

        return df

    def transform_for_predict(self, tweets, keep_words, keepn_tweets=30):

        selected_tweets, scores = self.select_topn_tweets(
            list(tweets), keep_words, keep_topn=keepn_tweets
        )
        return selected_tweets

    def save_keep_words(self, path):
        with open(path, "wb") as f:
            pickle.dump(self.keep_words, f)

    def load_keep_words(self, path):
        with open(path, "rb") as f:
            data = pickle.load(f)
        return data

    def select_topn_tweets(self, tweet_list, keep_words, keep_topn):
        """Select top N tweets using Chi-Square"""

        temp_tweet_list = []
        temp_scores_list = []

        for user_tweets in tqdm(tweet_list, total=len(tweet_list)):
            tweet_scores = {}
            for tweet_idx, tweet in enumerate(user_tweets):
                tweet_score = 0
                for word in tweet.split():
                    if word.lower() in keep_words:
                        tweet_score += 1

                tweet_scores[tweet_idx] = tweet_score

            selected_tweet_idx = list(
                {
                    k: v
                    for k, v in sorted(
                        tweet_scores.items(), key=lambda item: item[1], reverse=True
                    )
                }.keys()
            )[:keep_topn]
            selected_tweet_scores = list(
                {
                    k: v
                    for k, v in sorted(
                        tweet_scores.items(), key=lambda item: item[1], reverse=True
                    )
                }.values()
            )[:keep_topn]
            temp_user_tweets = np.array(user_tweets)[selected_tweet_idx]
            temp_tweet_list.append(temp_user_tweets)
            temp_scores_list.append(selected_tweet_scores)

        return temp_tweet_list, temp_scores_list
