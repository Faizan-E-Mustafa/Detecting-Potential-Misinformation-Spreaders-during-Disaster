import re


def preprocess(tweet):
    """preprocessing for disaster dataset"""

    tweet = re.sub(r"# ?[A-Za-z0-9]+[^HASHTAG#|URL#|USER#]", "#HASHTAG# ", tweet)
    tweet = re.sub(r"https?:\/\/t.co\/[A-Za-z0-9]+", "#URL#", tweet)
    # https://stackoverflow.com/questions/2304632/regex-for-twitter-username/6351873
    tweet = re.sub(
        r"(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9-_]+)", "#USER#", tweet
    )
    return tweet
