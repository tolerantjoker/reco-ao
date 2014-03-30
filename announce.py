# -*- coding: UTF-8 -*-
'''
Created on 23 mars 2014

@author: tolerantjoker
'''

from scipy import sparse
from sklearn import decomposition
from sklearn.feature_extraction.text import HashingVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import numpy as np
from preprocessor import Preprocessor
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
        self.item_tags = self.vec.transform([self.description])
        #print(self.item_tags.toarray())
        return self.item_tags
    
    def get_topics(self):
        '''
        Détermine les affinités de l'appel d'offre avec les différents topics.
        On calcule les affinités par un calcul de similarité entre item-tags et tags-topics.
        '''
        self.item_topics = self.reco_sys.nmf_object.transform(self.item_tags)
#         self.item_topics = cosine_similarity(self.item_tags,
#                                              sparse.csr_matrix(np.array(self.reco_sys.tags_topics.components_)))
        return self.item_topics
