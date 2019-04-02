###第三步text处理：为断句做准本的text预处理

import pandas as pd
import numpy as np
import nltk
import re
from nltk.tokenize import word_tokenize, sent_tokenize

###这一部分我们为断句作准备，也就是为真正会用到的text作准备，最重要的操作是找到句子中的分割点
def sentenceClean3(self):
    result = self.lower()
    result = re.sub('as (\w+?) as', '\\1', result)
    result = re.sub('not only (\w+?), but also', '\\1 and ', result)
    result = re.sub('but\s', ' duanju ', result)
    result = re.sub('otherwise\s', ' duanju ', result)
    result = re.sub('[\.,!\?]', ' duanju ', result)
    result = re.sub('high\squality', 'great', result)
    result = re.sub('low\squality', 'bad', result)
    result = re.sub('fast food', 'fastfood', result)
    result = re.sub('n\'t\s', ' not', result)
    result = re.sub('\sstars|\sstar', 'stars', result)
    result = re.sub('0stars', 'zerostars', result)
    result = re.sub('1stars', 'onestars', result)
    result = re.sub('2stars', 'twostars', result)
    result = re.sub('3stars', 'threestars', result)
    result = re.sub('4stars', 'fourstars', result)
    result = re.sub('5stars', 'fivestars', result)
    result = re.sub('not\s', ' not', result)
    result = re.sub('never\s', ' never', result)
    return result
sentenceClean3('it\'s not as good as I want')
sentenceClean3('it\'s not only great, but also fantanstic')

qqExample = pd.read_csv('/Applications/Study/UWM/628/module2/qq.csv', index_col=0)
qqExample.head(5)
qqExample['text'] = qqExample['text'].apply(sentenceClean3)
qqExample.head(5)
qqExample.to_csv('/Applications/Study/UWM/628/module2/textUsing/transqq3.csv')

test = pd.read_csv('/Applications/Study/UWM/628/module2/chinesereview.csv')
test['text'] = test['text'].apply(sentenceClean3)
test.to_csv('/Applications/Study/UWM/628/module2/textUsing/transchinese3.csv')