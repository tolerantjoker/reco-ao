# -*- coding: UTF-8 -*-
'''
Created on 20 mars 2014

@author: tolerantjoker
'''
import os.path

from scipy import sparse
from sklearn import cross_validation, decomposition
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import announce
import client
import config
import db_entity
import numpy as np
import pandas as pd
from preprocessor import Preprocessor
import sklearn.metrics
import pylab as pl


class RecoSystem(object):
    '''
    classdocs
    '''
    class __Singleton:
        
        def __init__(self):
            '''
            Constructor
            '''
            self.THRESHOLD = 0.6  # Seuil pour accepter/rejetter la recommandation d'un appel d'offre
            
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

            self.nmf_object = decomposition.NMF(n_components=self.n_components)

            self.items_tags = None
            self.tags_topics = None
            self.clients_topics = None
            self.reco_df = None
        
        def split_train_test(self):
            if os.path.isfile(config.TRAIN_SET) and os.path.isfile(config.TEST_SET):
                self.train_set = joblib.load(config.TRAIN_SET)
                self.test_set = joblib.load(config.TEST_SET)
            else:
                self.attributed_announce_list = self.db.getAnnounceAttributed()
                self.unattributed_announce_list = self.db.getAnnounceAttributed()
                # self.announce_list = self.attributed_announce_list + self.unattributed_announce_list
                # self.train_set, self.test_set = cross_validation.train_test_split(self.announce_list)
                
#                 self.train_set, self.test_set = cross_validation.train_test_split(self.attributed_announce_list)
#                 self.test_set = self.test_set.tolist()
#                 self.test_set.extend(self.unattributed_announce_list)
#                 self.test_set = np.array(self.test_set)

                client_list = self.db.getClientList()
                client_train, client_test = (), ()
                for c in client_list:
                    client_obj = client.Client(params=c)
                    s = self.db.getClientAnnounces(c['id'])
                    train, test = cross_validation.train_test_split(s)
                    client_train += (train,)
                    client_test += (test,)
                    # On sauvegarde le training set du client
                    client_obj.train_test = list(train)
                    joblib.dump(client_obj.train_test, config.CLIENT_TRAIN_SET + str(client_obj.id) + '.save')
                    # On sauvegarde le test set du client
                    client_obj.test_set = list(test)
                    joblib.dump(client_obj.test_set, config.CLIENT_TEST_SET + str(client_obj.id) + '.save')
                self.train_set = np.concatenate(client_train)
                self.test_set = np.concatenate(client_test + (self.unattributed_announce_list,))
                
                # Sauvegarde du train set et du test set
                joblib.dump(self.train_set, config.TRAIN_SET)
                joblib.dump(self.test_set, config.TEST_SET)
        
        def get_items_tags(self):
            '''
            Génère la matrice items_tags à partir du 'train set'
            '''
            train_set_description = [a['title'] + a['description'] for a in self.train_set]
            self.items_tags = self.vec.fit_transform(train_set_description)
            # sauvegarde du vectorizer avec son vocabulaire 
            joblib.dump(self.vec, config.VEC_RECO)
        
        def get_tags_topics(self):
            '''
            Génère la matrice tags-topics à partir de la matrice items_tags
            '''
            if(os.path.isfile(config.NMF_OBJECT) and os.path.isfile(config.TAGS_TOPICS)):
                self.nmf_object = joblib.load(config.NMF_OBJECT)
                self.tags_topics = joblib.load(config.TAGS_TOPICS)
            else:
                self.get_items_tags()
                self.tags_topics = self.nmf_object.fit(self.items_tags)
                # self.tags_topics.components_ =  (1.0 / 50.0) * np.asarray(self.tags_topics.components_)
                joblib.dump(self.nmf_object, config.NMF_OBJECT)
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
                for a_client in self.client_list:
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
            item_topics = sparse.csr_matrix(np.array(item.get_topics()))
#             item_topics = item.get_topics()

            self.get_clients_topics()
            clients_topics = sparse.csr_matrix(np.array(self.clients_topics))
#             clients_topics = self.clients_topics
            
#             item_clients = chi2_kernel(item_topics, clients_topics)
            item_clients = cosine_similarity(item_topics, clients_topics)
            return item, item_clients
        
        def get_reco_df(self):
            '''
            Renvoit un pandas.DataFrame de la forme
                    ao1 ao2 ao3 ao4 ao5
            client1  x   x   x   x   x
            client2  x   x   x   x   x
            client3  x   x   x   x   x
            client4  x   x   x   x   x
            '''
            if os.path.isfile(config.RECO_DF):
                self.reco_df = joblib.load(config.RECO_DF)
            else:
                d = {}
                
                if self.client_list is None:
                    self.client_list = []
                    r = self.db.getClientList()
                    for t in r:
                        self.client_list.append(client.Client(t))
                    
                index = [c.id for c in self.client_list]
                
                for t in self.test_set:
                    ao = announce.Announce(t)
                    item, item_clients = self.get_item_clients(ao)
                    d[item.id] = item_clients.tolist()[0]
                
                self.reco_df = pd.DataFrame(d, index=index)
                joblib.dump(self.reco_df, config.RECO_DF)
            
            return self.reco_df
        
        def precision_recall(self):
            '''
            Renvoie la précision moyenne du système.
            '''
            self.precisions, self.recalls = [], []
            client_list = self.db.getClientList()
            clients = []
            for d in client_list:
                clients.append(client.Client(params=d))
                
            for c in clients:
                c.get_reco_list()
                precision, recall = c.precision_recall()
                self.precisions.append(precision)
                self.recalls.append(recall)

            return np.mean(self.precisions), np.mean(self.recalls)
        
        def precision_recall_curve(self):
            area = sklearn.metrics.auc(self.precisions, self.recalls, reorder=True)
            pl.clf()
            pl.plot(self.recalls, self.precisions, label='Precision-Recall curve')
            pl.xlabel('Recall')
            pl.ylabel('Precision')
            pl.ylim([0.0, 1.05])
            pl.xlim([0.0, 1.0])
            pl.title('Precision-Recall: AUC=%0.2f' % area)
            pl.legend(loc="lower left")
            pl.show()
        
    instance = None
    def __new__(cls):
        if RecoSystem.instance is None:
            RecoSystem.instance = RecoSystem.__Singleton()
        return RecoSystem.instance

    def __getattr__(self, attr):
        return getattr(self.instance, attr)
  
    def __setattr__(self, attr, val):
        return setattr(self.instance, attr, val)
