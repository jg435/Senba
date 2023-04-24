import requests
import config
import sys
import time

class SpamDetection:
    API_URL = "https://api-inference.huggingface.co/models/mariagrandury/roberta-base-finetuned-sms-spam-detection"
    headers = {"Authorization": f"Bearer {config.HF_API_KEY}"}
    loading_speed = 4
    loading_string = "."*6

    @staticmethod
    def query(payload):
        response = requests.post(SpamDetection.API_URL, headers=SpamDetection.headers, json=payload)
        while "error" in response.json()[0][0]:
            for char in SpamDetection.loading_string:
                sys.stdout.write(char)
                sys.stdout.flush()
                time.sleep(1.0/SpamDetection.loading_speed)
        return response.json()[0]

    @staticmethod
    def pipeline(raw_text):
        payload ={}
        payload["inputs"] = raw_text
        query_response = SpamDetection.query(payload)
        return query_response

# test_string = "Camera - You are awarded a SiPix Digital Camera! call 09061221066 fromm landline. Delivery within 28 days."
# model = SpamDetection()    
# print(model.pipeline(test_string))
