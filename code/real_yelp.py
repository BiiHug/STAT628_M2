import json
import pandas as pd
import numpy as np
import re

file3 = open('/Applications/Study/UWM/628/module2/data/business_train.json','r')
busTrain = file3.readlines()
file3.close()

for i in range(len(busTrain)):
    busTrain[i]=json.loads(busTrain[i])

dfBusTrain = pd.DataFrame.from_records(busTrain)
dfBusTrain.head(5)

def checkRes(self):
    result = False
    try:
        catList = self.lower().replace(" ", "").split(',')
        if ('restaurants'in catList) or ('restaurant'in catList):
            result=True
    except AttributeError:
        result = False
    return result

resIndex = np.where(dfBusTrain['categories'].apply(checkRes))
resIdList = dfBusTrain['business_id'].iloc[resIndex]

dfResTrain = dfBusTrain.iloc[resIndex]
dfResTrain.drop(['is_open', 'postal_code'],axis=1,inplace=True)

allCatList = []
def addCat(self):
    cat = re.sub('\s+|\)','',self.lower())
    cat = re.sub('&|/|\(',',',cat).split(',')
    allCatList.extend(cat)
dfResTrain['categories'].apply(addCat)

catSeries = pd.Series(allCatList)
catSeries.value_counts()
catSeries.value_counts()[catSeries.value_counts()>500]
