import roberta_base_case as roberta
import pandas as pd
import sklearn.metrics

df = pd.read_csv('manualTextMessageData.csv')
thing = df.iloc[1]

thisModel = roberta.Roberta

testString = "This is my test string"

testPipeline = thisModel.pipeline(testString)

def getHFScoreDictFromPipeline(pipelineData):
    sentimentDict = {}
    for i in range(len(pipelineData)):
        sentimentType = pipelineData[i]['label']
        sentimentDict[sentimentType] = pipelineData[i]['score']
    return sentimentDict


def getModelMSE(thisModel, manualDF):
    mse_list = []
    for _, row in manualDF.iterrows():
        try:
            myTextMessage = row['Text Message']
            thisQueryPipeline = thisModel.pipeline(myTextMessage)
            myModelScores = getHFScoreDictFromPipeline(thisQueryPipeline)
            myModelScoreArray = []
            myManualScoreArray = []
            for key in myModelScores:
                thisManualScore = row[key]
                thisModelScore = myModelScores[key]
                myManualScoreArray.append(float(thisManualScore))
                myModelScoreArray.append(float(thisModelScore))
            mse = sklearn.metrics.mean_squared_error(myManualScoreArray, myModelScoreArray)
            mse_list.append(mse)
        except ValueError or KeyError:
            print("Row that has the error:", row)
    overall_mse = sum(mse_list)
    print(f"Overall MSE for all rows: {overall_mse}")
    
getModelMSE(thisModel, df)