# -*- coding: UTF-8 -*-
'''
Created on 19 mars 2014

@author: tolerantjoker
'''

import db_entity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import decomposition
import reco_system
from preprocessor import Preprocessor

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
    
    def get_historic(self):
        with self.dbentity.conn.cursor() as cursor:
            query = '''SELECT announce FROM assignments WHERE company = ?'''
            params = (self.id,)
            cursor.execute(query, params)
            self.historic = cursor.fetchall()
            #self.historic = [i for i in historic if i in self.reco_sys.train]
            return self.historic
        
    def get_tags(self):
        vec = TfidfVectorizer(tokenizer=Preprocessor(),
                              max_features=self.reco_sys.n_feature,
                              vocabulary=self.reco_sys.items_tags.vocabulary_)
        self.client_tags = vec.fit_transform(self.historic)
    
    def get_topics(self):
        self.client_topics = decomposition.NMF(n_components=self.reco_sys.n_components).fit(self.client_tags)
        
