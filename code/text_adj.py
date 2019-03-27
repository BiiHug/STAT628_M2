import pandas as pd
import numpy as np
import nltk
import re
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords

uselessList = list(set(stopwords.words('english')).difference(set(['no','nor','not'])))
'to' in uselessList

def sentenceClean(self):
    result = self.lower()
    result = re.sub('\'s|\'m|\'re|\'d|\'ll|\'ve',' ',result)
    #注意这里使用|后一定pattern要填写完整
    result = re.sub('pretty|very|always|food|chinese', ' ', result)
    result = re.sub('high\squality', 'great', result)
    result = re.sub('low\squality', 'bad', result)
    result = re.sub('\samount|portion', 'amount', result)
    result = re.sub('serve', 'service', result)
    result = re.sub('[\.,\(\)\+:!\?#]',' ',result)
    ##这里前面加\s的目的是防止误删
    result = re.sub('\s\w+?n\'t[^\w]+?', ' not', result)
    result = ' '.join([w for w in word_tokenize(result) if w not in uselessList])
    result = re.sub('\sstars|\sstar', 'stars', result)
    result = re.sub('1stars', 'onestars', result)
    result = re.sub('2stars', 'twostars', result)
    result = re.sub('3stars', 'threestars', result)
    result = re.sub('4stars', 'fourstars', result)
    result = re.sub('5stars', 'fivestars', result)
    result = re.sub('\\d|\$', '', result)
    result = re.sub('\snot\s', ' not', result)
    result = re.sub('\snever\s', ' never', result)
    return result

sentenceClean('this was pretty pretty great!')
sentenceClean('that\'s pretty great!')
sentenceClean('that\'s pretty great! I will give it five stars')
sentenceClean('It\'s of really high quality')
sentenceClean('I didn\'t like this, I can\'t do this, i have no option')
sentenceClean('that\'s not ture food! it\'s not 5 stars worth! not $5 !')
sentenceClean('the best food food ever!I want to go to this place')

test = pd.read_csv('/Applications/Study/UWM/628/module2/textUsing/chineseAllReview.csv')
test.head(5)

sentenceClean(test.text[5])
test['text'] = test['text'].apply(sentenceClean)
test['text'][5]

test.to_csv('/Applications/Study/UWM/628/module2/textUsing/transchinese.csv')

qqExample = pd.read_csv('/Applications/Study/UWM/628/module2/qq.csv', index_col=0)
qqExample.head(5)
qqExample['text'] = qqExample['text'].apply(sentenceClean)
qqExample.head(5)
qqExample.to_csv('/Applications/Study/UWM/628/module2/textUsing/transqq.csv')
