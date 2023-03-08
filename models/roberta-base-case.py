import requests
import config
import sys
import time

API_TOKEN = config.HF_API_KEY

API_URL = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment-latest"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

loading_speed = 4
loading_string = "."*6

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	while ("error") in response.json()[0][0]:
		for index, char in enumerate(loading_string):
			sys.stdout.write(char)
			sys.stdout.flush()
			time.sleep(1.0/loading_speed)  
	return response.json()[0]

	
	
def pipeline(raw_text):
	payload ={}
	payload["inputs"] = raw_text
	query_response = query(payload)
	return query_response


output = pipeline("please I want this to work")
print(output)