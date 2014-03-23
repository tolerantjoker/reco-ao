'''
Created on 23 mars 2014

@author: tolerantjoker
'''

import reco_system
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import decomposition
from preprocessor import Preprocessor

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
        
    def get_tags(self):
        vec = TfidfVectorizer(tokenizer=Preprocessor(),
                              max_features=self.n_feature,
                              vocabulary=self.reco_sys.items_tags.vocabulary_)
        self.item_tags = vec.fit_transform([self.description])
    
    def get_topics(self):
        self.item_topics = decomposition.NMF(n_components=self.reco_sys.n_components).fit(self.item_tags)
