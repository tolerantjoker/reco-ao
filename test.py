# -*- coding: UTF-8 -*-
'''
Created on 23 dec. 2013

@author: tolerantjoker
'''

from sklearn.feature_extraction.text import TfidfVectorizer
import oursql
import db_config
import analyzer

conn = oursql.connect(host=db_config.db_config['host'], user=db_config.db_config['user'],
                                       passwd=db_config.db_config['password'], db=db_config.db_config['db'])
res = []
with conn.cursor(oursql.DictCursor) as cursor:
                query = '''SELECT * FROM announces LIMIT 0,50'''
                cursor.execute(query)
                res = cursor.fetchall()
corpus = [a['description'] for a in res]

vec = TfidfVectorizer(tokenizer=analyzer.Analyzer(), max_features=500)
bag_of_words = vec.fit_transform(corpus)
 
# for word, value in vec.vocabulary_.items():
#     print(word + ' : ' + str(value))

feature_names = vec.get_feature_names()
rows = bag_of_words.nonzero()[0]
cols = bag_of_words.nonzero()[1]
indices = zip(rows, cols)
    
word_frequencies = [(feature_names[col], bag_of_words[row, col]) for row, col in indices]
for k, v in sorted(word_frequencies, key=lambda x:x[1], reverse=True):
    print(str(k) + ' = ' + str(v))
