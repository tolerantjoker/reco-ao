# -*- coding: UTF-8 -*-
'''
Created on 23 mars 2014

@author: tolerantjoker
'''

from preprocessor import Preprocessor
from scipy import sparse
from sklearn import decomposition
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import reco_system

class Announce(object):
    '''
    classdocs
    '''

    def __init__(self, params):
        '''
        Constructor
        '''
        self.id = params['id']
        self.title = params['title']
        self.description = params['description']
    
        self.reco_sys = reco_system.RecoSystem()
        self.item_tags = None
        self.item_topics = None
        
#         self.vec = TfidfVectorizer(tokenizer=Preprocessor(),
#                               max_features=self.reco_sys.n_feature,
#                               vocabulary=self.reco_sys.vec.vocabulary_.keys())
#         self.vec = HashingVectorizer(tokenizer=Preprocessor(),
#                             vocabulary=self.reco_sys.vec.vocabulary_.keys(),
#                             non_negative=True)
        self.vec = self.reco_sys.vec
        
    def get_tags(self):
        '''
        Génère le vecteur item-tags de l'appel d'offre
        '''
        self.item_tags = self.vec.fit_transform([self.description])
        return self.item_tags
    
    def get_topics(self):
        '''
        Détermine les affinités de l'appel d'offre avec les différents topics.
        On calcule les affinités par un calcul de similarité entre item-tags et tags-topics.
        '''
        # self.item_topics = decomposition.NMF(n_components=self.reco_sys.n_components).fit(self.item_tags)
        self.item_topics = cosine_similarity(self.item_tags,
                                             sparse.csr_matrix(np.array(self.reco_sys.tags_topics.components_)))
        return self.item_topics
