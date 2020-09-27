import xml.etree.ElementTree as ET
import pandas as pd


def read_data(path):
    """read data from xml files"""

    tweets_paths = [i for i in path.glob("*.xml")]
    targets_path = [i for i in path.glob("*.txt")][0]
    tweets = []
    user_ids = []
    # read tweets from xml files
    for file_path in tweets_paths:
        file_name = file_path.stem
        tree = ET.parse(file_path)
        root = tree.getroot()
        documents = root.findall("./documents/")
        user_tweets = [doc.text for doc in documents]

        tweets.append(user_tweets)
        user_ids.append(file_name)

    # get target mapping
    with open(targets_path) as f:
        content = f.read()
        content = content.split("\n")
        target_map = {}
        for i in content:
            try:
                user_id, target = i.split(":::")
            except:
                continue
            target_map[user_id] = int(target)
    # prepare dataframe
    df = pd.DataFrame({"user_id": user_ids, "tweets": tweets})
    df["target"] = df.user_id.map(target_map)

    return df
