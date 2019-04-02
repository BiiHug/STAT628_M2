###第二步text处理：对text进行打分的text预处理

import pandas as pd
import numpy as np
import nltk
import re
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords

uselessList = list(set(stopwords.words('english')).difference(set(['no','nor','not','only'])))

###这里我们为adj打分作准备，sentenceClean2在sentenceClean的基础上增加了去缩写，去标点，去stopwords等操作，目的是为了让text更加整洁，尽量提高adj的得分
def sentenceClean2(self):
    result = self.lower()
    result = re.sub('as (\w+?) as', '\\1', result)
    result = re.sub('not only (\w+?), but also', '\\1 and ', result)
    result = re.sub('\'s|\'m|\'re|\'d|\'ll|\'ve', ' ', result)
    result = re.sub('fast food', 'fastfood', result)
    result = re.sub('pretty|very|always|food|chinese', ' ', result)
    result = re.sub('high\squality', 'great', result)
    result = re.sub('low\squality', 'bad', result)
    result = re.sub('[\.,\(\)\+:!\?#]', ' ', result)
    result = re.sub('n\'t\s', ' not', result)
    result = re.sub('\sstars|\sstar', 'stars', result)
    result = re.sub('0stars', 'zerostars', result)
    result = re.sub('1stars', 'onestars', result)
    result = re.sub('2stars', 'twostars', result)
    result = re.sub('3stars', 'threestars', result)
    result = re.sub('4stars', 'fourstars', result)
    result = re.sub('5stars', 'fivestars', result)
    result = re.sub('\\d|\$', '', result)
    result = re.sub('not\s', ' not', result)
    result = re.sub('never\s', ' not', result)
    result = ' '.join([w for w in word_tokenize(result) if w in adjWordsList])
    return result

sentenceClean2('this was pretty pretty great!')
sentenceClean2('that\'s pretty great!')
sentenceClean2('that\'s pretty great! I will give it five stars')
sentenceClean2('It\'s of really high quality')
sentenceClean2('I didn\'t like this, I can\'t do this, i have no option')
sentenceClean2('that\'s not ture food! it\'s not 5 stars worth! not $5 !')
sentenceClean2('the best food food ever!I want to go to this place')

sentenceClean2('that\'s not ture food! it\'s not 5 stars worth! not $5 !')
sentenceClean2('The server here is quick and friendly!')
sentenceClean2('This is not as good as others!')
sentenceClean2('This is really oily fast food!')


test = pd.read_csv('/Applications/Study/UWM/628/module2/textUsing/chineseAllReview.csv')
test.head(5)
test['text'] = test['text'].apply(sentenceClean2)
test['text'][5]
test.to_csv('/Applications/Study/UWM/628/module2/textUsing/transchinese2.csv')

qqExample = pd.read_csv('/Applications/Study/UWM/628/module2/qq.csv', index_col=0)
qqExample.head(5)
qqExample['text'] = qqExample['text'].apply(sentenceClean2)
qqExample.head(5)
qqExample.to_csv('/Applications/Study/UWM/628/module2/textUsing/transqq2.csv')
