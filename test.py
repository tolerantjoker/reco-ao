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

vec = TfidfVectorizer(tokenizer=analyzer.Analyzer(), min_df=0, max_df=1)
bag_of_words = vec.fit_transform(corpus)
 
for word, value in sorted(vec.vocabulary_.items(), key=lambda x:x[1], reverse=True):
    print(word + ' : ' + str(value))
