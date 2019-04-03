###第一步text处理：提取adj的text预处理

import pandas as pd
import numpy as np
import nltk
import re
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords

uselessList = list(set(stopwords.words('english')).difference(set(['no','nor','not','only'])))

###这里的text预处理不能进行去标点、去stopwords等操作！因为我们需要进行词性标注，去掉这些内容可能会破坏句子完整性
def sentenceClean(self):
    result = self.lower()
    result = re.sub('pretty|very|always|food|chinese', ' ', result)
    result = re.sub('not so', 'not', result)
    result = re.sub('high\squality', 'great', result)
    result = re.sub('low\squality', 'bad', result)
    result = re.sub('n\'t\s', ' not', result)
    result = re.sub('\sstars|\sstar', 'stars', result)
    result = re.sub('0stars', 'zerostars', result)
    result = re.sub('1stars', 'onestars', result)
    result = re.sub('2stars', 'twostars', result)
    result = re.sub('3stars', 'threestars', result)
    result = re.sub('4stars', 'fourstars', result)
    result = re.sub('5stars', 'fivestars', result)
    result = re.sub('not\s', ' not', result)
    result = re.sub('never\s', ' not', result)
    return result

sentenceClean('It wasn\'t great.')
sentenceClean('It\'s a five stars restaurant!')
sentenceClean('The service here is of high quality')

test = pd.read_csv('/Applications/Study/UWM/628/module2/textUsing/chineseAllReview.csv')
test['text'] = test['text'].apply(sentenceClean)
test.to_csv('/Applications/Study/UWM/628/module2/textUsing/transchinese.csv')

adjList = ['JJ','JJR','JJS','VBN']

def detact_adj(self):
    testBag = nltk.pos_tag(word_tokenize(self))
    selectedBag = list(pd.Series([x[0] for x in testBag]).iloc[np.where([x[1] in adjList for x in testBag])])
    return selectedBag

testExample = pd.read_csv('/Applications/Study/UWM/628/module2/textUsing/transchinese.csv', index_col=0)
testExample.index = range(0,len(testExample))

i = 9
testExample.text[i]
detact_adj(testExample.text[i])
detact_adj('it is overcooked')
nltk.pos_tag(word_tokenize('It\'s a fivestars restaurant!'))
detact_adj('It\'s a fivestars restaurant!')
detact_adj('It was notdelicious at all!')
detact_adj('The service here is of great!')



allText = '. '.join(testExample.text)
adjWordsList = detact_adj(allText)
adjWordsList = [w for w in adjWordsList if w not in uselessList]
adjWordsList = list(pd.read_csv('/Applications/Study/UWM/628/module2/textUsing/chineseadjs.csv', index_col=0).words)
'notgreat' in adjWordsList
'notgood' in adjWordsList
'notdelicious' in adjWordsList
'fivestars' in adjWordsList
adjWordsList[5:10]

data = {'words': adjWordsList}
df = pd.DataFrame(data)
df.to_csv('/Applications/Study/UWM/628/module2/textUsing/chineseadjs.csv')