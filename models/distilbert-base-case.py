import requests
import config
import sys
import time

API_TOKEN = config.HF_API_KEY

API_URL = "https://api-inference.huggingface.co/models/bhadresh-savani/distilbert-base-uncased-emotion"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

loading_speed = 4
loading_string = "."*6
def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	while response.json()[0][0].has_key("error"):
		for index, char in enumerate(loading_string):
			sys.stdout.write(char)
			sys.stdout.flush()
			time.sleep(1.0/loading_speed)
	return response.json()

	
output = query({
	"inputs": "I like you. I love you",
})