import alert_scores
import roberta_base_case as roberta
import distilbert_base_case as distilbert
import json
import numpy as np
from sklearn.metrics import mean_squared_error as mse

class Sentiment_Model:
    model_dict = {
        "roberta":  roberta.Roberta,
        "distilbert": distilbert.Distilbert          
    }

    ALERT_SCORES, ALERT_FILENAMES = alert_scores.get_alert_scores_and_filenames()

    @staticmethod
    def get_all_sentiments_as_dict(input_string):
        #this is a dictionary that contains all of the sentiment values
        full_sentiment_dict = {}
        for model in Sentiment_Model.model_dict.values():
            #this outputs an array of dictionaries. each dictionary contains 1 sentiment value
            this_pipeline = model.pipeline(input_string)
            for sentiment_dict in this_pipeline:
                value_dict = {sentiment_dict['label']: sentiment_dict['score']}
                full_sentiment_dict.update(value_dict)

        return full_sentiment_dict
            
            
    @staticmethod
    def run(input_string):
        sentiment_dict = Sentiment_Model.get_all_sentiments_as_dict(input_string)

        json_object  = json.dumps(sentiment_dict, indent = 4)
        return json_object

    @staticmethod
    def pair_output_with_alert(input_string):

        sentiment_dict = Sentiment_Model.get_all_sentiments_as_dict(input_string)
        SENTIMENT_COLS = ['positive', 'negative', 'neutral', 'love', 'joy', 'sadness', 'anger', 'surprise', 'fear']

        sentiment_scores = []
        for col in SENTIMENT_COLS:
            sentiment_scores.append(sentiment_dict[col])

        NUM_ALERTS = len(Sentiment_Model.ALERT_SCORES)

        sentiment_scores_full = [sentiment_scores for _ in range(NUM_ALERTS)]
        mse_full = mse(Sentiment_Model.ALERT_SCORES, sentiment_scores_full, multioutput='raw_values')

        min_mse_index = np.argmin(mse_full)
        alert_filename = Sentiment_Model.ALERT_FILENAMES[min_mse_index]

        return alert_filename
#         json_alert_filename  = json.dumps(alert_filename)
#         return json_alert_filename


def pair_output_with_alert(input_string):
    model = Sentiment_Model()

    sentiment_dict = model.get_all_sentiments_as_dict(input_string)
    SENTIMENT_COLS = ['positive', 'negative', 'neutral', 'love', 'joy', 'sadness', 'anger', 'surprise', 'fear']

    sentiment_scores = []
    for col in SENTIMENT_COLS:
        sentiment_scores.append(sentiment_dict[col])

    NUM_ALERTS = len(model.ALERT_SCORES)

    sentiment_scores_full = [sentiment_scores for _ in range(NUM_ALERTS)]
    mse_full = mse(model.ALERT_SCORES, sentiment_scores_full, multioutput='raw_values')

    min_mse_index = np.argmin(mse_full)
    alert_filename = model.ALERT_FILENAMES[min_mse_index]

    return alert_filename
