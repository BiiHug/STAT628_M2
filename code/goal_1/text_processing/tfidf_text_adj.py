###这是试图做adj的tfidf的情况下的一个copy
###第二步text处理：对text进行打分的text预处理

import pandas as pd
import numpy as np
import nltk
import re
from nltk.tokenize import word_tokenize, sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

###这里我们为adj打分作准备，sentenceClean2在sentenceClean的基础上增加了去缩写，去标点，去stopwords等操作，目的是为了让text更加整洁，尽量提高adj的得分
def tfidf_sentenceClean2(self):
    result = self.lower()
    result = re.sub('as (\w+?) as', '\\1', result)
    result = re.sub('not only (\w+?), but also', '\\1 and ', result)
    result = re.sub('\'s|\'m|\'re|\'d|\'ll|\'ve',' ',result)
    result = re.sub('fast food', 'fastfood', result)
    result = re.sub('pretty|very|always|food|chinese', ' ', result)
    result = re.sub('high\squality', 'great', result)
    result = re.sub('low\squality', 'bad', result)
    result = re.sub('[\.,\(\)\+:!\?#]',' ',result)
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

tfidf_sentenceClean2('this was pretty pretty great!')
tfidf_sentenceClean2('that\'s pretty great!')
tfidf_sentenceClean2('that\'s pretty great! I will give it five stars')
tfidf_sentenceClean2('It\'s of really high quality')
tfidf_sentenceClean2('I didn\'t like this, I can\'t do this, i have no option')
tfidf_sentenceClean2('that\'s not ture food! it\'s not 5 stars worth! not $5 !')
tfidf_sentenceClean2('The server here is quick and friendly!')

tfidf_test = pd.read_csv('/Applications/Study/UWM/628/module2/textUsing/chineseAllReview.csv')
tfidf_test.head(5)
tfidf_sentenceClean2(tfidf_test.text[5])
tfidf_test['text'] = tfidf_test['text'].apply(tfidf_sentenceClean2)
tfidf_test['text'][5]

text_for_analysis = tfidf_test.text
bag_of_words = count_vectorizer.fit_transform(text_for_analysis)
feature_names = count_vectorizer.get_feature_names()
pd.DataFrame(bag_of_words.toarray(), columns = feature_names)
#TFIDF

tfidf_vectorizer = TfidfVectorizer()
values = tfidf_vectorizer.fit_transform(text_for_analysis)

# Show the Model as a pandas DataFrame
feature_names = tfidf_vectorizer.get_feature_names()
res_df=pd.DataFrame(values.toarray(), columns = feature_names)

res_df.to_csv('/Applications/Study/UWM/628/module2/textUsing/tfidfchinese.csv')

