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

qqExample = pd.read_csv('/Applications/Study/UWM/628/module2/qq.csv', index_col=0)
qqExample.index = range(0,len(qqExample))

i = 3
qqExample.text[i]
nltk.pos_tag(word_tokenize(qqExample.text[i]))
st.tag(word_tokenize(qqExample.text[i]))
st.tag_sents([sent_tokenize(qqExample.text[i])])

qqAll = '. '.join(qqExample.text)
len(qqAll)
nltk.pos_tag(word_tokenize(qqAll))
st.tag(word_tokenize(qqAll))
st.tag_sents([sent_tokenize(qqAll)])

test = pd.read_csv('/Applications/Study/UWM/628/module2/textUsing/chineseAllReview.csv')
test.head(5)

testAll = '. '.join(test.text)
len(testAll)
mangyiba = st.tag(word_tokenize(testAll))
