# -*- coding: UTF-8 -*-
'''
Created on 19 mars 2014

@author: tolerantjoker
'''

from preprocessor import Preprocessor
from scipy import sparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import chi2_kernel
import db_entity
import numpy as np
import oursql
import reco_system
from sklearn import decomposition

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
#         self.vec = HashingVectorizer(tokenizer=Preprocessor(),
#                                      vocabulary=self.reco_sys.vec.vocabulary_.keys(),
#                                      non_negative=True)
#         self.vec = self.reco_sys.vec
        
    def get_historic(self):
        '''
        Retourne la liste des appels d'offres qui ont été attribués au client.
        '''
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
#             return self.historic
        
    def get_tags(self):
        '''
        Renvoie le modèle 'bag-of-words' d'un client.
        Ce modèle est construit à partir de l'historique des appels d'offres du client.
        '''
        self.get_historic()
        historic = [e['description'] for e in self.historic]
        self.client_tags = self.vec.fit_transform(historic)
    
    def get_topics(self):
        '''
        Renvoie les affinités du client avec chaque topic
        '''
        # self.client_topics = decomposition.NMF(n_components=self.reco_sys.n_components).fit(self.client_tags)
        self.get_tags()
        self.client_topics = cosine_similarity(self.client_tags,
                                               sparse.csr_matrix(np.array(self.reco_sys.tags_topics.components_)))
        self.client_topics = np.mean(np.asarray(self.client_topics), axis=0)
        return self.client_topics
