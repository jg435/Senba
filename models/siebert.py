from transformers import pipeline
import pandas as pd
import sklearn.metrics
import numpy as np

sentiment_analysis = pipeline("sentiment-analysis",model="siebert/sentiment-roberta-large-english")
text_messages_df = pd.read_csv('data/final_text_messages.csv')
text_messages = text_messages_df['Text Message']
myModelScoreArray = list()
myManualScoreArray = list()
mse_list = list()
#print(np.where(text_messages == 'U can call me now...')[0][0])
      
for message in text_messages:
    model_result = sentiment_analysis(message)
    if float(text_messages_df.loc[np.where(text_messages == message)[0][0], 'positive'])!=0 and float(text_messages_df.loc[np.where(text_messages == message)[0][0], 'positive'])!=0:
        myModelScoreArray.append(float(model_result[0]['score']))
        if model_result[0]['label']=='POSITIVE':
            myManualScoreArray.append(float(text_messages_df.loc[np.where(text_messages == message)[0][0], 'positive'])/(float(text_messages_df.loc[np.where(text_messages == message)[0][0], 'positive'])+float(text_messages_df.loc[np.where(text_messages == message)[0][0], 'negative'])))
        elif model_result[0]['label']=='NEGATIVE':
            myManualScoreArray.append(float(text_messages_df.loc[np.where(text_messages == message)[0][0], 'negative'])/(float(text_messages_df.loc[np.where(text_messages == message)[0][0], 'positive'])+float(text_messages_df.loc[np.where(text_messages == message)[0][0], 'negative'])))
    else:
        myModelScoreArray.append(0.5)
        myManualScoreArray.append(0.5)
    mse = sklearn.metrics.mean_squared_error(myManualScoreArray, myModelScoreArray)
    mse_list.append(mse)
overall_mse = sum(mse_list)
print("Overall MSE is ", overall_mse)

