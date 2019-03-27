import pandas as pd
import numpy as np
import nltk
import re
from os.path import expanduser
from nltk import StanfordPOSTagger
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.corpus import brown
import spacy


home = expanduser("~")
_path_to_model = home + '/stanford-postagger/models/english-bidirectional-distsim.tagger'
_path_to_jar = home + '/stanford-postagger/stanford-postagger.jar'

st = StanfordPOSTagger(_path_to_model, _path_to_jar)

shitThing = ['.',',','-','(',')',':']

test = pd.read_csv('/Applications/Study/UWM/628/module2/textUsing/chineseAllReview.csv')
test.head(5)

tagList = ['JJ','JJR','JJS','RB','RBR','RBS','VB','VBD','VBG','VBN','VBP','VBZ']
def wordTrans(self):
    testBag = nltk.pos_tag(word_tokenize(self))
    #testBag = st.tag(word_tokenize(self))
    selectedBag = list(pd.Series(list(dict(testBag).keys())).iloc[np.where([x in tagList for x in list(dict(testBag).values())])])
    selectResult = ' '.join(selectedBag)
    return sentenceClean2(selectResult)


def sentenceClean(self):
    result = self.lower()
    result = re.sub('\'s','',result)
    result = re.sub('\'m', '', result)
    result = re.sub('\'re', '', result)
    result = re.sub('\sis\s', '', result)
    result = re.sub('\sam\s', '', result)
    result = re.sub('\sare\s', '', result)
    result = re.sub('\swas\s', '', result)
    result = re.sub('[\.,\(\)\+:!]','',result)
    result = re.sub('\s\w+?n\'t[^\w]+?', ' not', result)
    result = re.sub('no\s', 'no',result)
    result = re.sub('not\s', 'not', result)
    return result

def sentenceClean2(self):
    result = self.lower()
    result = re.sub('\'s', ' ', result)
    result = re.sub('\'m', ' ', result)
    result = re.sub('\'re', ' ', result)
    result = re.sub('\sis\s', ' ', result)
    result = re.sub('\sam\s', ' ', result)
    result = re.sub('\sare\s', ' ', result)
    result = re.sub('\swas\s', ' ', result)
    result = re.sub('[\.,\(\)\+:!-]','',result)
    result = re.sub('\w+?\sn\'t[^\w]+?', ' not', result)
    result = re.sub('no\s', 'no',result)
    result = re.sub('not\s', 'not', result)
    return result

test['text'] = test['text'].apply(sentenceClean)
test['text'].head(7)

test.to_csv('/Applications/Study/UWM/628/module2/textUsing/transchinese.csv')

qqExample = pd.read_csv('/Applications/Study/UWM/628/module2/qq.csv', index_col=0)
qq7 = qqExample.text[39571]

qq7_1 = sent_tokenize(qq7)[-1]
sentenceClean(qq7_1)

tofu_1 = sent_tokenize(qq7)[1]
sentenceClean(tofu_1)
tags_tofu = nltk.pos_tag(sentenceClean(tofu_1))
nltk.ne_chunk(tags_tofu)

qq_15 = qqExample.text[39579]
not_1 = sent_tokenize(qq_15)[2]
sentenceClean(qq_15)

nltk.pos_tag(word_tokenize('it is a clean and beautiful restaurant otherwise with average service and very well kept restrooms'))
nltk.pos_tag(word_tokenize('i would definitely not recommend this restaurant'))
nltk.pos_tag(word_tokenize('i won\'t like this restaurant'))
nltk.pos_tag(word_tokenize('this was really great!'))
nltk.pos_tag(word_tokenize('boring,flavorless and spicy'))
nltk.pos_tag(word_tokenize('it is boring,flavorless and spicy'))
st.tag(word_tokenize('boring,flavorless and spicy'))


home = expanduser("~")
_path_to_model = home + '/stanford-postagger/models/english-bidirectional-distsim.tagger'
_path_to_jar = home + '/stanford-postagger/stanford-postagger.jar'

st = StanfordPOSTagger(_path_to_model, _path_to_jar)

nltk.pos_tag(word_tokenize('the tofu is pretty cold, flavorless, and a bit slimy.'))
st.tag(word_tokenize('the tofu is pretty cold, flavorless, and a bit slimy.'))

nltk.pos_tag(word_tokenize('i would definitely not recommend this restaurant'))
st.tag(word_tokenize('it\'s over-cooked!'))

nltk.pos_tag(word_tokenize(qq7))
st.tag(word_tokenize(qq7))

nltk.pos_tag(word_tokenize(qq_15))
testBag = st.tag(word_tokenize(qq_15))
selectedBag = list(pd.Series(list(dict(testBag).keys())).iloc[np.where([x in tagList for x in list(dict(testBag).values())])])
selectResult = ' '.join(selectedBag)
sentenceClean2(selectResult)

wordTrans(qq7)
test['text'] = test['text'].apply(wordTrans)
test.head(7)
test.to_csv('/Applications/Study/UWM/628/module2/textUsing/transchinese.csv')

qqExample['text'] = qqExample['text'].apply(wordTrans)
qqExample.head(7)
qqExample.to_csv('/Applications/Study/UWM/628/module2/textUsing/transqq.csv')

words_tag =  dict(nltk.corpus.nps_chat.tagged_words())
words_tag['spicy']

