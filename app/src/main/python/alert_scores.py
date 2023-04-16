import pandas as pd
from os.path import dirname, join

def get_alert_dict():
    # file_path = "./final_notification_ratings.csv"
    file_path = join(dirname(__file__), "final_notification_ratings.csv")

    # dictionary of alert filename: score num array
    alert_dict = {}
    df = pd.read_csv(file_path, header=0)

    for _, row in df.iterrows():
        alert_dict[row['Notification Sound']] = row[1:].tolist()

    return alert_dict

def get_alert_scores_and_filenames():
    # file_path = "./final_notification_ratings.csv"
    file_path = join(dirname(__file__), "final_notification_ratings.csv")

    # list of score num arrays
    df = pd.read_csv(file_path, header=0)
    sentiment_cols = ['positive', 'negative', 'neutral', 'love', 'joy', 'sadness', 'anger', 'surprise', 'fear']
    alert_scores = df[sentiment_cols].values.tolist()

    # list of alert filenames in order
    alert_order = df['Notification Sound'].values.tolist()

    return alert_scores, alert_order
