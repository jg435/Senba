import requests
import config
import sys
import time

class Roberta:
    API_URL = "https://api-inference.huggingface.co/models/siebert/sentiment-roberta-large-english"
    headers = {"Authorization": f"Bearer {config.HF_API_KEY}"}
    loading_speed = 4
    loading_string = "."*6

    @staticmethod
    def query(payload):
        response = requests.post(Roberta.API_URL, headers=Roberta.headers, json=payload)
        while "error" in response.json()[0][0]:
            for char in Roberta.loading_string:
                sys.stdout.write(char)
                sys.stdout.flush()
                time.sleep(1.0/Roberta.loading_speed)
        return response.json()[0]

    @staticmethod
    def pipeline(raw_text):
        payload ={}
        payload["inputs"] = raw_text
        query_response = Roberta.query(payload)
        return query_response