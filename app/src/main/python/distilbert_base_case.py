import requests
import config
import sys
import time

class Distilbert:
    API_URL = "https://api-inference.huggingface.co/models/bhadresh-savani/distilbert-base-uncased-emotion"
    headers = {"Authorization": f"Bearer {config.HF_API_KEY}"}
    loading_speed = 4
    loading_string = "."*6

    @staticmethod
    def query(payload):
        response = requests.post(Distilbert.API_URL, headers=Distilbert.headers, json=payload)
        while "error" in response.json()[0][0]:
            for char in Distilbert.loading_string:
                sys.stdout.write(char)
                sys.stdout.flush()
                time.sleep(1.0/Distilbert.loading_speed)
        return response.json()[0]

    @staticmethod
    def pipeline(raw_text):
        payload ={}
        payload["inputs"] = raw_text
        query_response = Distilbert.query(payload)
        return query_response