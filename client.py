# -*- coding: UTF-8 -*-
'''
Created on 19 mars 2014

@author: tolerantjoker
'''
import numpy as np
from scipy import sparse
from sklearn.metrics.pairwise import cosine_similarity

import db_entity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import decomposition
import reco_system
from preprocessor import Preprocessor
import oursql

class Client(object):
    '''
    classdocs
    '''

    def __init__(self, params):
        '''
        Constructor
        '''
        self.dbentity = db_entity.DB_entity()
        self.id = params['id']
        self.name = params['name']
        self.url = params['url']
        
        self.reco_sys = reco_system.RecoSystem()
        self.historic = None
        self.client_tags = None
        self.client_topics = None
        
        self.vec = TfidfVectorizer(tokenizer=Preprocessor(),
                              max_features=self.reco_sys.n_feature,
                              vocabulary=self.reco_sys.vec.vocabulary_.keys())
    
    def get_historic(self):
        with self.dbentity.conn.cursor(oursql.DictCursor) as cursor:
            query = '''
            SELECT assignments.announce, announces.description
            FROM assignments
            JOIN announces ON assignments.announce = announces.id
            WHERE company = ?'''
            params = (self.id,)
            cursor.execute(query, params)
            historic = cursor.fetchall()
            # print(historic)
            announces_train_id = [e['id'] for e in self.reco_sys.train_set]
            self.historic = [e for e in historic if e['announce'] in announces_train_id]
            return self.historic
        
    def get_tags(self):
        historic = [e['description'] for e in self.historic]
        self.client_tags = self.vec.fit_transform(historic)
        return self.client_tags.toarray()
    
    def get_topics(self):
        # self.client_topics = decomposition.NMF(n_components=self.reco_sys.n_components).fit(self.client_tags)
        self.client_topics = cosine_similarity(self.client_tags,
                                               sparse.csr_matrix(np.array(self.reco_sys.tags_topics.components_)))
        self.client_topics = np.mean(self.client_topics, axis=0)
        return self.client_topics
