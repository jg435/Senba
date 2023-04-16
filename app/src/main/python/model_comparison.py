import pandas as pd
import random
import csv

#DO NOT RUN THIS
#EVER
#DO. NOT. RUN. THIS. FILE. OR. WE'RE. FUCKED.

df = pd.read_csv('models/spam.csv', encoding = 'ISO-8859-1')[['v1','v2']]
text_messages = list(df[df['v1'] == 'ham']['v2'].reset_index()['v2'])
sampled_text_messages = list()
num_text_messages = 100
total_texts_added = 0

index_list = []

while total_texts_added <= 100:
    index = random.randint(0, len(text_messages))
    if text_messages[index] not in sampled_text_messages:
        sampled_text_messages.append(text_messages[index])
    
    total_texts_added+=1

with open('models/text_messages.csv', 'w', newline='') as f:
  writer = csv.writer(f)
  writer.writerow(['Text Message', 'Manual or Machine', 'Positive', 'Negative', 'Neutral', 'Love', 'Joy', 'Sadness', 'Anger', 'Surprise', 'Fear'])
  for message in sampled_text_messages:
    row_list = [message, 'Manual']
    writer.writerow(row_list)
     
#print(sampled_text_messages)

#text message, love, joy, sadness, anger, surprise, fear, postive, negative, neutral
    



