import constants
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

    # Initialize constants
    ALERT_FILENAMES = list(constants.ALERT_DICT.keys())
    ALERT_SCORES = np.swapaxes(np.array(list(constants.ALERT_DICT.values())),0,1)
    NUM_ALERTS = len(ALERT_FILENAMES)
    ROBERTA_ALERT_SCORES = ALERT_SCORES[:3, :]
    DISTILBERT_ALERT_SCORES = ALERT_SCORES[3:, :]
    SENTIMENT_COLS = ['positive', 'negative', 'neutral', 'love', 'joy', 'sadness', 'anger', 'surprise', 'fear']


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


def pair_output_with_alert(input_string):
    model = Sentiment_Model()

    sentiment_dict = model.get_all_sentiments_as_dict(input_string)

    sentiment_scores_full = []
    for col in model.SENTIMENT_COLS:
        sentiment_scores_full.append([sentiment_dict[col]]*model.NUM_ALERTS)

    mse_full = mse(model.ALERT_SCORES, sentiment_scores_full, multioutput='raw_values')

    min_mse_index = np.argmin(mse_full)
    alert_filename = model.ALERT_FILENAMES[min_mse_index]

    return alert_filename


def pair_output_with_alert_separate_mse(input_string):
    model = Sentiment_Model()

    sentiment_dict = model.get_all_sentiments_as_dict(input_string)

    sentiment_scores_full = []
    for col in model.SENTIMENT_COLS:
        sentiment_scores_full.append([sentiment_dict[col]]*model.NUM_ALERTS)

    # 1) MSE for ROBERTA: 3 labels (pos, neg, neutral)
    roberta_scores_full = np.array(sentiment_scores_full)[:3, :]
    mse_roberta = mse(model.ROBERTA_ALERT_SCORES, roberta_scores_full, multioutput='raw_values')

    # 2) MSE for DISTILBERT: 6 labels (love, joy, sadness, anger, surprise, fear)
    distilbert_scores_full = np.array(sentiment_scores_full)[3:, :]
    mse_distilbert = mse(model.DISTILBERT_ALERT_SCORES, distilbert_scores_full, multioutput='raw_values')

    if np.min(mse_roberta) < np.min(mse_distilbert):
        print(f'Roberta selected: {mse_roberta}')
        min_mse_index = np.argmin(mse_roberta)
    else:
        print(f'Distilbert selected: {mse_distilbert}')
        min_mse_index = np.argmin(mse_distilbert)

    alert_filename = model.ALERT_FILENAMES[min_mse_index]
    return alert_filename
