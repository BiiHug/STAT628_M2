import json
import pandas as pd
import numpy as np
import re
from gensim.corpora.dictionary import Dictionary
import operator
import matplotlib.pyplot as plt

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
dfResTrain.index = range(len(dfResTrain))
dfResTrain.drop(['is_open', 'postal_code'],axis=1,inplace=True)


##处理categories，首先得到一个大的list：catListFrame
##可以发现categories有上百种，并不像attr一样只有20多种，所以可能需要进行主题提取
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


##处理attributes，
###首先得到一个attr的keylist，看看到底有哪些attr
attrKeyList = []
def getKeys(self):
    try:
        attrKeyList.extend(self.keys())
    except AttributeError:
        next
dfResTrain['attributes'].apply(getKeys)
###现在倾向于只保留>25000条记录的attr,一共有17个
pd.Series(attrKeyList).value_counts()
validAttrs = pd.Series(attrKeyList).value_counts().index[:17]

###挑选出validAttr，得到一个大的list：attrListFrame
attrListFrame = []
def sub_dict(dct, keys, default=None):
    return dict([(key, dct.get(key, default)) for key in keys])
def addAttr(self):
    try:
        validKeys = list(set(list(self.keys())).intersection(set(validAttrs)))
        validSubDict = sub_dict(self, validKeys)
        attrListFrame.append(validSubDict)
    except AttributeError:
        attrListFrame.append({})
dfResTrain['attributes'].apply(addAttr)

###attrListFrame可以非常方便地转化为dataframe
dfAttrFrame = pd.DataFrame.from_records(attrListFrame)
dfAttrFrame.head(5)

###仔细来看看每一个attr的情况
def getAttrs(x, attr):
    return x.get(attr, '')
takeoutList = [getAttrs(x, 'RestaurantsTakeOut') for x in attrListFrame]
###空白表示有5000+家店是没有takeout记录的，None表示有45家店takeout记录显示为None？？？
pd.Series(takeoutList).value_counts()
priceList = [getAttrs(x, 'RestaurantsPriceRange2') for x in attrListFrame]
pd.Series(priceList).value_counts()
good4groupList = [getAttrs(x, 'RestaurantsGoodForGroups') for x in attrListFrame]
pd.Series(good4groupList).value_counts()
good4kidsList = [getAttrs(x, 'GoodForKids') for x in attrListFrame]
pd.Series(good4kidsList).value_counts()
reserveList = [getAttrs(x, 'RestaurantsReservations') for x in attrListFrame]
pd.Series(reserveList).value_counts()
deliverList = [getAttrs(x, 'RestaurantsDelivery') for x in attrListFrame]
pd.Series(deliverList).value_counts()
deliverList = [getAttrs(x, 'RestaurantsDelivery') for x in attrListFrame]
pd.Series(deliverList).value_counts()
outdoorseatList = [getAttrs(x, 'OutdoorSeating') for x in attrListFrame]
pd.Series(outdoorseatList).value_counts()
tvList = [getAttrs(x, 'HasTV') for x in attrListFrame]
pd.Series(tvList).value_counts()
bikeparkList = [getAttrs(x, 'BikeParking') for x in attrListFrame]
pd.Series(bikeparkList).value_counts()
catersList = [getAttrs(x, 'Caters') for x in attrListFrame]
pd.Series(catersList).value_counts()
cardsList = [getAttrs(x, 'BusinessAcceptsCreditCards') for x in attrListFrame]
pd.Series(cardsList).value_counts()

###下列这几个是有大小写及元字符的问题，修改一下就好，值得关注的是应该分几级
clothList = [getAttrs(x, 'RestaurantsAttire') for x in attrListFrame]
pd.Series(clothList).value_counts()
alcoholList = [getAttrs(x, 'Alcohol') for x in attrListFrame]
pd.Series(alcoholList).value_counts()
noiseList = [getAttrs(x, 'NoiseLevel') for x in attrListFrame]
pd.Series(noiseList).value_counts()
wifiList = [getAttrs(x, 'WiFi') for x in attrListFrame]
pd.Series(wifiList).value_counts()

###这两个应该怎么处理？有处理的必要吗？有留下来的必要吗？
carparkList = [getAttrs(x, 'BusinessParking') for x in attrListFrame]
pd.Series(carparkList).value_counts()
ambienceList = [getAttrs(x, 'Ambience') for x in attrListFrame]
pd.Series(ambienceList).value_counts()
###carpark试水
def carCan(x):
    result = ''
    if x[1] == True:
        result = x[0]
    return result
test = list(set([carCan(x) for x in list(eval(carparkList[6]).items())]) - set(['']))
###根据停车方便程度将车辆友好度分为0，1，2级
def carFriend(self):
    try:
        canList = list(set([carCan(x) for x in list(eval(self).items())]) - set(['']))
        if len(canList)>0:
            if len(set(canList) - set(['lot','street']))>0:
                return 2
            else:
                return 1
        else:
            return 0
    except AttributeError:
        return None
    except SyntaxError:
        return None
###得到carFriendList
carFriendList = list(map(carFriend, carparkList))
pd.Series(carFriendList).value_counts()


##处理hours
dfResTrain['hours'].head(5)
###天数？
daysList = []
def checkDays(self):
    try:
        daysList.append(len(self.keys()))
    except AttributeError:
        daysList.append(None)
dfResTrain['hours'].apply(checkDays)
###可以发现大部分都是5天以上的，我认为在这里依据天数进行划分是没有意义的
pd.Series(daysList).value_counts()

###时间段？
hoursList = []
def checkHours(self):
    try:
        hoursList.append(list(self.values()))
    except AttributeError:
        hoursList.append(None)
dfResTrain['hours'].apply(checkHours)

###计算时间段长度，这里只取第一天的长度
def calcuHours(self):
    try:
        openTime = pd.to_datetime(self[0].split('-')[0], format="%H:%M")
        closeTime = pd.to_datetime(self[0].split('-')[1], format="%H:%M")
        return (closeTime - openTime).seconds/3600
    except TypeError:
        return None

hoursRange = list(map(calcuHours, hoursList))
pd.Series(hoursRange).describe()
###这里最好画个图吧，我的air不行了
###大于15小时，昼夜餐厅
len((np.where(pd.Series(hoursRange)>15))[0])
###小于6小时，特殊营业餐厅
len((np.where(pd.Series(hoursRange)<6))[0])

def cateHours(self):
    type = 'all_day'
    try:
        openTime = pd.to_datetime(self[0].split('-')[0], format="%H:%M")
        closeTime = pd.to_datetime(self[0].split('-')[1], format="%H:%M")
        range = (closeTime - openTime).seconds/3600
        if range > 15:
            type = '24_hours'
        if range < 6:
            if closeTime < pd.to_datetime('15:00', format="%H:%M"):
                type = 'brunch'
            else:
                type = 'dinner'
    except TypeError:
        type = None
    return type
hoursCate = list(map(cateHours, hoursList))
pd.Series(hoursCate).value_counts()