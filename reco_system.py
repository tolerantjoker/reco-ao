# -*- coding: UTF-8 -*-
'''
Created on 20 mars 2014

@author: tolerantjoker
'''
import client
import db_entity
import numpy as np
from sklearn import cross_validation
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from preprocessor import Preprocessor
from sklearn import decomposition
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import chi2_kernel
from scipy import sparse
from sklearn.externals import joblib
import os.path
import config

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
            
            self.n_feature = 500
            self.n_components = 20
            
           
            self.client_list = None
            self.attributed_announce_list = None
            self.unattributed_announce_list = None
            self.announce_list = None
            
            self.train_set = None
            self.test_set = None
            
            if(os.path.isfile(config.VEC_RECO)):
                self.vec = joblib.load(config.VEC_RECO)
            else:
                self.vec = TfidfVectorizer(tokenizer=Preprocessor(), max_features=self.n_feature)
                # joblib.dump(self.vec, config.VEC_RECO)
#                 self.vec = HashingVectorizer(tokenizer=Preprocessor(),
#                                              n_features=self.n_feature,
#                                              non_negative=True)
            self.items_tags = None
            self.tags_topics = None
            self.clients_topics = None
        
        def split_train_test(self):
            if os.path.isfile(config.TRAIN_SET) and os.path.isfile(config.TEST_SET):
                self.train_set = joblib.load(config.TRAIN_SET)
                self.test_set = joblib.load(config.TEST_SET)
            else:
                self.attributed_announce_list = self.db.getAnnounceAttributed()
                self.unattributed_announce_list = self.db.getAnnounceAttributed()
                self.announce_list = self.attributed_announce_list + self.unattributed_announce_list
                self.train_set, self.test_set = cross_validation.train_test_split(self.announce_list)
                # Sauvegarde du train set et du test set
                joblib.dump(self.train_set, config.TRAIN_SET)
                joblib.dump(self.test_set, config.TEST_SET)
        
        def get_items_tags(self):
            '''
            Génère la matrice items_tags à partir du 'train set'
            '''
            train_set_description = [a['description'] for a in self.train_set]
            self.items_tags = self.vec.fit_transform(train_set_description)
            # sauvegarde du vectorizer avec son vocabulaire 
            joblib.dump(self.vec, config.VEC_RECO)
        
        def get_tags_topics(self):
            '''
            Génère la matrice tags-topics à partir de la matrice items_tags
            '''
            if(os.path.isfile(config.TAGS_TOPICS)):
                self.tags_topics = joblib.load(config.TAGS_TOPICS)
            else:
                self.get_items_tags()
                self.tags_topics = decomposition.NMF(n_components=self.n_components).fit(self.items_tags)
                #self.tags_topics.components_ =  (1.0 / 50.0) * np.asarray(self.tags_topics.components_)
                joblib.dump(self.tags_topics, config.TAGS_TOPICS)
        
        def get_clients_topics(self):
            '''
            Génère la matrice clients-topics à partir de l'historique de chaque client et de la matrice tags-topics
            '''
            if(os.path.isfile(config.CLIENTS_TOPICS)):
                self.clients_topics = joblib.load(config.CLIENTS_TOPICS)
            else:                
                self.client_list = []
                r = self.db.getClientList()
                for t in r:
                    self.client_list.append(client.Client(t))
                
                self.clients_topics = []
                for a_client in self.client_list[:-1]:
#                     historic = a_client.get_historic()
#                     client_tags = a_client.get_tags()
                    client_topics = a_client.get_topics()            
                    self.clients_topics.append(client_topics)
                
                joblib.dump(self.clients_topics, config.CLIENTS_TOPICS)
        
        def get_item_clients(self, item):
            '''
            Génère les affinités des clients vis à vis d'un appel d'offre entrant
            '''
            item.get_tags()
#             item_topics = sparse.csr_matrix(np.array(item.get_topics()))
            item_topics = item.get_topics()

            self.get_clients_topics()
#             clients_topics = sparse.csr_matrix(np.array(self.clients_topics))
            clients_topics = self.clients_topics
            
            item_clients = chi2_kernel(item_topics, clients_topics)
            #item_clients = cosine_similarity(item_topics, clients_topics)
            return item, item_clients
                     
    
    instance = None
    def __new__(cls):
        if RecoSystem.instance is None:
            RecoSystem.instance = RecoSystem.__Singleton()
        return RecoSystem.instance

    def __getattr__(self, attr):
        return getattr(self.instance, attr)
  
    def __setattr__(self, attr, val):
        return setattr(self.instance, attr, val)
