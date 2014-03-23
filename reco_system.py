# -*- coding: UTF-8 -*-
'''
Created on 20 mars 2014

@author: tolerantjoker
'''

import db_entity
import numpy as np
from sklearn import cross_validation
from sklearn.feature_extraction.text import TfidfVectorizer
from preprocessor import Preprocessor
from sklearn import decomposition
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse
from gensim.models import tfidfmodel

class RecoSystem(object):
    '''
    classdocs
    '''
    class __Singleton:
        def __init__(self):
            '''
            Constructor
            '''
            self.db = db_entity.DB_entity()
            
            self.n_feature = 100
            self.n_components = 10
           
            self.client_list = None
            self.attributed_announce_list = None
            self.unattributed_announce_list = None
            self.announce_list = None
            
            self.train_set = None
            self.test_set = None
            
            self.vec = TfidfVectorizer(tokenizer=Preprocessor(), max_features=self.n_feature)
            self.items_tags = None
            self.tags_topics = None
        
        def split_train_test(self):
            self.attributed_announce_list = self.db.getAnnounceAttributed()
            self.unattributed_announce_list = self.db.getAnnounceAttributed()
            self.announce_list = self.attributed_announce_list + self.unattributed_announce_list
            self.train_set, self.test_set = cross_validation.train_test_split(self.attributed_announce_list)
            train_set_description = [a['description'] for a in self.train_set]
        
        def get_items_tags(self):
            train_set_description = [a['description'] for a in self.train_set]
            self.items_tags = self.vec.fit_transform(train_set_description)
        
        def get_tags_topics(self):
            '''
            Génère la matrice tags-topics à partir du corpus de 13000 appels d'offres
            '''
            self.tags_topics = decomposition.NMF(n_components=self.n_components).fit(self.items_tags)
        
        def get_clients_topics(self):
            '''
            Génère la matrice clients-topics à partir de l'historique de chaque client et de la matrice tags-topics
            '''
            pass
        
        def get_recommendation_list(self):
            '''
            Génère une liste de client pour un appel d'offre entrant donné.
            '''
            pass
        
    instance = None
    def __new__(cls):
        if RecoSystem.instance is None:
            RecoSystem.instance = RecoSystem.__Singleton()
        return RecoSystem.instance

    def __getattr__(self, attr):
        return getattr(self.instance, attr)
  
    def __setattr__(self, attr, val):
        return setattr(self.instance, attr, val)
