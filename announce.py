'''
Created on 23 mars 2014

@author: tolerantjoker
'''
import numpy as np
from scipy import sparse

import reco_system
from preprocessor import Preprocessor
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import decomposition
from sklearn.metrics.pairwise import cosine_similarity


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
        
        self.vec = TfidfVectorizer(tokenizer=Preprocessor(),
                              max_features=self.n_feature,
                              vocabulary=self.reco_sys.vec.vocabulary_.keys())
        
    def get_tags(self):
        self.item_tags = self.vec.fit_transform([self.description])
    
    def get_topics(self):
        # self.item_topics = decomposition.NMF(n_components=self.reco_sys.n_components).fit(self.item_tags)
        self.item_topics = cosine_similarity(self.item_tags,
                                             sparse.csr_matrix(np.array(self.reco_sys.tags_topics.components_)))
