import roberta_base_case as roberta
import distilbert_base_case as distilbert
import json

class Sentiment_Model:
    model_dict = {
        "roberta":  roberta.Roberta,
        "distilbert": distilbert.Distilbert          
    }


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