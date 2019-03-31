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
    result = re.sub('n\'t\s', ' not', result)
    result = re.sub('\sstars|\sstar', 'stars', result)
    result = re.sub('0stars', 'onestars', result)
    result = re.sub('1stars', 'onestars', result)
    result = re.sub('2stars', 'twostars', result)
    result = re.sub('3stars', 'threestars', result)
    result = re.sub('4stars', 'fourstars', result)
    result = re.sub('5stars', 'fivestars', result)
    result = re.sub('\snot\s', ' not', result)
    result = re.sub('\snever\s', ' never', result)
    return result

test = pd.read_csv('/Applications/Study/UWM/628/module2/textUsing/chineseAllReview.csv')
test['text'] = test['text'].apply(sentenceClean2)
test.to_csv('/Applications/Study/UWM/628/module2/textUsing/transchinese2.csv')

#nltk.pos_tag(word_tokenize('jason is a really nice guy.'))
tagList = ['JJ','JJR','JJS','RB','RBR','RBS','VB','VBD','VBG','VBN','VBP','VBZ']
nounList = ['NN', 'NNS']
adjList = ['JJ','JJR','JJS','VBN']

def detact_adj(self):
    testBag = nltk.pos_tag(word_tokenize(self))
    selectedBag = list(pd.Series([x[0] for x in testBag]).iloc[np.where([x[1] in adjList for x in testBag])])
    return selectedBag

testExample = pd.read_csv('/Applications/Study/UWM/628/module2/textUsing/transchinese2.csv', index_col=0)
testExample.index = range(0,len(testExample))

i = 9
testExample.text[i]
detact_adj(testExample.text[i])
detact_adj('it is overcooked')
nltk.pos_tag(word_tokenize(testExample.text[i]))
nltk.pos_tag(word_tokenize('it is overcooked'))


allText = '. '.join(testExample.text)
adjWordsList = detact_adj(allText)
adjWordsList = [w for w in adjWordsList if w not in uselessList]
data = {'words': adjWordsList}
df = pd.DataFrame(data)
df.to_csv('/Applications/Study/UWM/628/module2/textUsing/chineseadjs.csv')