import json
import pandas as pd
import numpy as np
import re
from gensim.corpora.dictionary import Dictionary


#这一个part是在处理商家数据
##读入数据
file3 = open('/Applications/Study/UWM/628/module2/data/business_train.json','r')
busTrain = file3.readlines()
file3.close()
for i in range(len(busTrain)):
    busTrain[i]=json.loads(busTrain[i])
dfBusTrain = pd.DataFrame.from_records(busTrain)
dfBusTrain.head(5)


##选出restaurant
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
###这里的idlist给出了restaurant的id
resIdList = dfBusTrain['business_id'].iloc[resIndex]
dfResTrain = dfBusTrain.iloc[resIndex]
dfResTrain.drop(['is_open', 'postal_code'],axis=1,inplace=True)


##处理categories，首先得到一个大的list：catListFrame
dfResTrain['categories'].head(5)
catListFrame = []
def addCat(self):
    cat = re.sub('\s+|\)','',self.lower())
    cat = list(set(re.sub('&|/|\(',',',cat).split(',')) - set(['restaurants', 'restaurant', 'food']))
    catListFrame.append(cat)
dfResTrain['categories'].apply(addCat)
###catListFrame可转化为dataframe
dfCatFrame = pd.DataFrame.from_records(catListFrame)
dfCatFrame.head(5)
###catListFrame也可转化为series, 并进一步转化为词袋形式进行LDA
restaurants_dictionary = Dictionary(pd.Series(catListFrame))
restaurants_corpus = [restaurants_dictionary.doc2bow(text) for text in pd.Series(catListFrame)]
restaurants_corpus[2]
###待解决：是否只能用LDA？是否需要LDA？可以尝试一下LSA？

