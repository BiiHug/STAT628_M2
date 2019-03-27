import pandas as pd
import numpy as np
import nltk
import re
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk import StanfordPOSTagger
from os.path import expanduser

home = expanduser("~")
_path_to_model = home + '/stanford-postagger/models/english-bidirectional-distsim.tagger'
_path_to_jar = home + '/stanford-postagger/stanford-postagger.jar'

st = StanfordPOSTagger(_path_to_model, _path_to_jar)

def sentenceClean2(self):
    result = self.lower()
    result = re.sub('high\squality', 'great', result)
    result = re.sub('low\squality', 'bad', result)
    result = re.sub('serve', 'service', result)
    result = re.sub('fast food', 'fastfood', result)
    result = re.sub('\s\w+?n\'t[^\w]+?', ' not', result)
    result = re.sub('\sstars|\sstar', 'stars', result)
    result = re.sub('1stars', 'onestars', result)
    result = re.sub('2stars', 'twostars', result)
    result = re.sub('3stars', 'threestars', result)
    result = re.sub('4stars', 'fourstars', result)
    result = re.sub('5stars', 'fivestars', result)
    result = re.sub('\snot\s', ' not', result)
    result = re.sub('\snever\s', ' never', result)
    return result

qqExample = pd.read_csv('/Applications/Study/UWM/628/module2/qq.csv', index_col=0)
qqExample['text'] = qqExample['text'].apply(sentenceClean2)
qqExample.to_csv('/Applications/Study/UWM/628/module2/textUsing/transqq2.csv')

#nltk.pos_tag(word_tokenize('jason is a really nice guy.'))
tagList = ['JJ','JJR','JJS','RB','RBR','RBS','VB','VBD','VBG','VBN','VBP','VBZ']
nounList = ['NN', 'NNS']

def detact_noun(self):
    testBag = nltk.pos_tag(word_tokenize(self))
    selectedBag = list(pd.Series(list(dict(testBag).keys())).iloc[np.where([x in nounList for x in list(dict(testBag).values())])])
    return selectedBag

qqExample = pd.read_csv('/Applications/Study/UWM/628/module2/textUsing/transqq2.csv', index_col=0)
qqExample.index = range(0,len(qqExample))

detact_noun(qqExample.text[41])
nltk.pos_tag(word_tokenize(qqExample.text[41]))
st.tag(word_tokenize(qqExample.text[41]))

qqExample['text'] = qqExample['text'].apply(detact_noun)
qqExample.head(5)
qqExample.to_csv('/Applications/Study/UWM/628/module2/textUsing/nounsqq.csv')
