import json
import pandas as pd
import numpy as np
import re

# chinese_business part
file3 = open('/Applications/Study/UWM/628/module2/data/business_train.json','r')
busTrain = file3.readlines()
file3.close()
for i in range(len(busTrain)):
    busTrain[i]=json.loads(busTrain[i])
dfBusTrain = pd.DataFrame.from_records(busTrain)
dfBusTrain.head(5)

def checkChinese(self):
    result = False
    try:
        catList = self.lower().replace(" ", "").split(',')
        if 'chinese'in catList:
            result=True
    except AttributeError:
        result = False
    return result
chineseIndex = np.where(dfBusTrain['categories'].apply(checkChinese))
chineseIdList = dfBusTrain['business_id'].iloc[chineseIndex]
dfChineseTrain = dfBusTrain.iloc[chineseIndex]
dfChineseTrain.index = range(len(dfChineseTrain))
dfChineseTrain.drop(['is_open', 'postal_code'],axis=1,inplace=True)


dfChineseTrain['categories'].head(5)
chineseCatListFrame = []
def addChineseCat(self):
    cat = re.sub('\s+|\)','',self.lower())
    cat = list(set(re.sub('&|/|\(',',',cat).split(',')) - set(['restaurants', 'restaurant', 'food','chinese']))
    chineseCatListFrame.extend(cat)
dfChineseTrain['categories'].apply(addChineseCat)
###和其他类型的餐厅相比，chinese的第二标签比较少，针对性更强
pd.Series(chineseCatListFrame).value_counts()[:20]


chineseAttrKeyList = []
def getChineseKeys(self):
    try:
        chineseAttrKeyList.extend(self.keys())
    except AttributeError:
        next
dfChineseTrain['attributes'].apply(getChineseKeys)
pd.Series(chineseAttrKeyList).value_counts()
validChineseAttrs = pd.Series(chineseAttrKeyList).value_counts().index[:18]

chineseAttrListFrame = []
def sub_dict(dct, keys, default=None):
    return dict([(key, dct.get(key, default)) for key in keys])
def addChineseAttr(self):
    try:
        validKeys = list(set(list(self.keys())).intersection(set(validChineseAttrs)))
        validSubDict = sub_dict(self, validKeys)
        chineseAttrListFrame.append(validSubDict)
    except AttributeError:
        chineseAttrListFrame.append({})
dfChineseTrain['attributes'].apply(addChineseAttr)
chineseAttrListFrame[0]

dfchineseAttrFrame = pd.DataFrame.from_records(chineseAttrListFrame)
dfchineseAttrFrame.head(5)

def getAttrs(x, attr):
    try:
        return x.get(attr, '')
    except AttributeError:
        return ''

takeoutList = [getAttrs(x, 'RestaurantsTakeOut') for x in chineseAttrListFrame]
###空白表示有5000+家店是没有takeout记录的，None表示有45家店takeout记录显示为None？？？
pd.Series(takeoutList).value_counts()
priceList = [getAttrs(x, 'RestaurantsPriceRange2') for x in chineseAttrListFrame]
pd.Series(priceList).value_counts()
good4groupList = [getAttrs(x, 'RestaurantsGoodForGroups') for x in chineseAttrListFrame]
pd.Series(good4groupList).value_counts()
good4kidsList = [getAttrs(x, 'GoodForKids') for x in chineseAttrListFrame]
pd.Series(good4kidsList).value_counts()
reserveList = [getAttrs(x, 'RestaurantsReservations') for x in chineseAttrListFrame]
pd.Series(reserveList).value_counts()
deliverList = [getAttrs(x, 'RestaurantsDelivery') for x in chineseAttrListFrame]
pd.Series(deliverList).value_counts()
outdoorseatList = [getAttrs(x, 'OutdoorSeating') for x in chineseAttrListFrame]
pd.Series(outdoorseatList).value_counts()
tvList = [getAttrs(x, 'HasTV') for x in chineseAttrListFrame]
pd.Series(tvList).value_counts()
bikeparkList = [getAttrs(x, 'BikeParking') for x in chineseAttrListFrame]
pd.Series(bikeparkList).value_counts()
catersList = [getAttrs(x, 'Caters') for x in chineseAttrListFrame]
pd.Series(catersList).value_counts()
cardsList = [getAttrs(x, 'BusinessAcceptsCreditCards') for x in chineseAttrListFrame]
pd.Series(cardsList).value_counts()

###下列这几个是有大小写及元字符的问题，修改一下就好，值得关注的是应该分几级
def removeUnicode(self):
    try:
        return re.sub('u|\'','',self)
    except TypeError:
        return None

clothList = [getAttrs(x, 'RestaurantsAttire') for x in chineseAttrListFrame]
pd.Series(clothList).value_counts()
dfchineseAttrFrame['RestaurantsAttire'] = dfchineseAttrFrame['RestaurantsAttire'].apply(removeUnicode)
alcoholList = [getAttrs(x, 'Alcohol') for x in chineseAttrListFrame]
pd.Series(alcoholList).value_counts()
dfchineseAttrFrame['Alcohol'] = dfchineseAttrFrame['Alcohol'].apply(removeUnicode)
noiseList = [getAttrs(x, 'NoiseLevel') for x in chineseAttrListFrame]
pd.Series(noiseList).value_counts()
dfchineseAttrFrame['NoiseLevel'] = dfchineseAttrFrame['NoiseLevel'].apply(removeUnicode)
wifiList = [getAttrs(x, 'WiFi') for x in chineseAttrListFrame]
pd.Series(wifiList).value_counts()
dfchineseAttrFrame['WiFi'] = dfchineseAttrFrame['WiFi'].apply(removeUnicode)

carparkList = [getAttrs(x, 'BusinessParking') for x in chineseAttrListFrame]
pd.Series(carparkList).value_counts()
ambienceList = [getAttrs(x, 'Ambience') for x in chineseAttrListFrame]
pd.Series(ambienceList).value_counts()
good4mealList = [getAttrs(x, 'GoodForMeal') for x in chineseAttrListFrame]
pd.Series(good4mealList).value_counts()


##处理park数据
def carCan(x):
    result = ''
    if x[1] == True:
        result = x[0]
    return result

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
dfchineseAttrFrame['BusinessParking'] = carFriendList


##处理hours
dfChineseTrain['hours'].head(5)
###天数？
daysList = []
def checkDays(self):
    try:
        daysList.append(len(self.keys()))
    except AttributeError:
        daysList.append(None)
dfChineseTrain['hours'].apply(checkDays)
###可以发现大部分都是5天以上的，我认为在这里依据天数进行划分是没有意义的
pd.Series(daysList).value_counts()

###时间段？
hoursList = []
def checkHours(self):
    try:
        hoursList.append(list(self.values()))
    except AttributeError:
        hoursList.append(None)
dfChineseTrain['hours'].apply(checkHours)

###计算时间段长度，这里只取第一天的长度
def calcuHours(self):
    try:
        openTime = pd.to_datetime(self[0].split('-')[0], format="%H:%M")
        closeTime = pd.to_datetime(self[0].split('-')[1], format="%H:%M")
        return (closeTime - openTime).seconds/3600
    except TypeError:
        return None

hoursRange = list(map(calcuHours, hoursList))
pd.Series(hoursRange).value_counts()
pd.Series(hoursRange).describe()
###这里最好画个图吧，我的air不行了
###大于15小时，昼夜餐厅
len((np.where(pd.Series(hoursRange)>=15))[0])
###小于6小时，特殊营业餐厅
len((np.where(pd.Series(hoursRange)<=6))[0])

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
dfChineseTrain['hours'] = hoursCate


##最后得到处理过后的dfchineseAttrFrame，删掉了'Ambience', 'GoodForMeal'，同时与删掉了'attributes', 'categories','latitude','longitude'
##的dfChineseTrain进行合并
dfchineseAttrFrameMerge = dfchineseAttrFrame.drop(['Ambience', 'GoodForMeal'],axis=1)
dfChineseTrainMerge = dfChineseTrain.drop(['attributes', 'categories','latitude','longitude'],axis=1)
dfChineseBusMerge = pd.concat([dfChineseTrainMerge, dfchineseAttrFrameMerge], axis=1)



# chinese_review part

file = open('/Applications/Study/UWM/628/module2/data/review_train.json','r')
reviewTrain = file.readlines()
file.close()
for i in range(len(reviewTrain)):
    reviewTrain[i]=json.loads(reviewTrain[i])
dfReviewTrain = pd.DataFrame.from_records(reviewTrain)
dfReviewTrain.head(5)

##得到chinese restaurants的评论
chineseIdList = list(chineseIdList)
def getChinese(self):
    if self in chineseIdList:
        return True
    else:
        return False
### !!!为什么这一行会奇慢无比？？？
chineseReviewIndex = np.where(dfReviewTrain['business_id'].apply(getChinese))
len(chineseReviewIndex[0])
dfChineseReviewTrain = dfReviewTrain.iloc[resReviewIndex]
dfChineseReviewTrain.index = range(len(dfResReviewTrain))
dfChineseReviewTrain.head(5)


##准备与business数据合并
dfChineseReviewTrain = dfChineseReviewTrain.loc[:,['business_id','stars','text']]
dfChineseFinalMerge = pd.merge(dfChineseBusMerge, dfChineseReviewTrain, on='business_id')
len(dfChineseFinalMerge)
dfChineseFinalMerge.head(5)
dfChineseFinalMerge.to_csv('/Applications/Study/UWM/628/module2/chinesereview.csv')



