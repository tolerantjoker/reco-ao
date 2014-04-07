# -*- coding: UTF-8 -*-
'''
Created on 23 dec. 2013

@author: tolerantjoker
'''

from sklearn.feature_extraction.text import TfidfVectorizer
import oursql
import db_config
import preprocessor

conn = oursql.connect(host=db_config.db_config['host'], user=db_config.db_config['user'],
                                       passwd=db_config.db_config['password'], db=db_config.db_config['db'])
res = []
with conn.cursor(oursql.DictCursor) as cursor:
                query = '''SELECT * FROM announces'''
                cursor.execute(query)
                res = cursor.fetchall()
corpus = [a['description'] for a in res]

vec = TfidfVectorizer(tokenizer=preprocessor.Preprocessor(), max_df=1, min_df=0)
vec.fit(corpus)

for word, value in sorted(vec.vocabulary_.items(), key=lambda x:x[1], reverse=True):
    print(word + ' : ' + str(value))
