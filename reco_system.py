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
from scipy import sparse
from test import n_feature

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
            
            #self.vec = TfidfVectorizer(tokenizer=Preprocessor(), max_features=self.n_feature)
            self.vec = HashingVectorizer(tokenizer=Preprocessor(),
                                         n_features=self.n_feature,
                                         non_negative=True)
            self.items_tags = None
            self.tags_topics = None
            self.clients_topics = None
        
        def split_train_test(self):
            self.attributed_announce_list = self.db.getAnnounceAttributed()
            self.unattributed_announce_list = self.db.getAnnounceAttributed()
            self.announce_list = self.attributed_announce_list + self.unattributed_announce_list
            self.train_set, self.test_set = cross_validation.train_test_split(self.announce_list)
            #train_set_description = [a['description'] for a in self.train_set]
        
        def get_items_tags(self):
            '''
            Génère la matrice items_tags à partir du 'train set'
            '''
            train_set_description = [a['description'] for a in self.train_set]
            self.items_tags = self.vec.fit_transform(train_set_description)
        
        def get_tags_topics(self):
            '''
            Génère la matrice tags-topics à partir de la matrice items_tags
            '''
            self.tags_topics = decomposition.NMF(n_components=self.n_components).fit(self.items_tags)
        
        def get_clients_topics(self):
            '''
            Génère la matrice clients-topics à partir de l'historique de chaque client et de la matrice tags-topics
            '''
            if self.clients_topics is not None:
                return self.clients_topics
            
            self.client_list = []
            r = self.db.getClientList()
            for t in r:
                self.client_list.append(client.Client(t))
            
            self.clients_topics = []
            for a_client in self.client_list[:-1]:
                historic = a_client.get_historic()
#                 print(len(historic))
                client_tags = a_client.get_tags()
#                 print(len(client_tags))
                client_topics = a_client.get_topics()
#                 print(client_topics)
            
                self.clients_topics.append(client_topics)
            return self.clients_topics
        
        def get_item_clients(self, item):
            '''
            Génère les affinités des clients vis à vis d'un appel d'offre entrant
            '''
            item.get_tags()
            item_topics = sparse.csr_matrix(np.array(item.get_topics()))
#             print("item_topics=")
#             print(item_topics)
            clients_topics = sparse.csr_matrix(np.array(self.get_clients_topics()))
#             print("clients_topics")
#             print(clients_topics)
            item_clients = cosine_similarity(item_topics, clients_topics)
            return item, item_clients
            ### Récupérer les identifiants des clients
            
        def get_recommendation_list(self, item):
            '''
            Génère une liste de client pour un appel d'offre entrant donné.
            '''
            item, item_clients = self.get_item_clients()
            ### TODO ###
                
                
            
    
    instance = None
    def __new__(cls):
        if RecoSystem.instance is None:
            RecoSystem.instance = RecoSystem.__Singleton()
        return RecoSystem.instance

    def __getattr__(self, attr):
        return getattr(self.instance, attr)
  
    def __setattr__(self, attr, val):
        return setattr(self.instance, attr, val)
