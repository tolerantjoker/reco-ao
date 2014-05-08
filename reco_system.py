# -*- coding: UTF-8 -*-
'''
Created on 20 mars 2014

:author: François Royer & Valentin Lhommeau
'''

import os.path

from scipy import sparse
from sklearn import cross_validation, decomposition
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from analyzer import Analyzer
import announce
import client
import config
import db_entity
import numpy as np
import pandas as pd

class RecoSystem(object):
    '''
    Classe qui représente une instance du système de recommandation.
    
    :ivar THRESHOLD: le seuil pour accepter la recommandation d'un appel d'offres.
    :ivar db: une instance de gestion de la base de données.
    :ivar min_df: le nombre minimum de documents dans lesquels un mot doit apparaître pour être conservé dans 
    le BagOfWords (pour plus de détails cf. la documentation de scikit-learn).
    :ivar max_df: le nombre minimum de documents dans lesquels un mot doit apparaître pour être conservé dans 
    le BagOfWords (pour plus de détails cf. la documentation de scikit-learn).
    :ivar n_feature: le nombre maximal de mots qui sont conservé dans le BagOfWords.
    :ivar n_components: le nombre de composantes/thèmes/topics à conserver dans la matrice tags_topics.
    :ivar client_list: la liste des clients.
    :ivar attributed_announce_list: la liste de toutes les annonces attribuées.
    :ivar unattributed_announce_list: la liste de toutes les annonces non attribuées.
    :ivar announce_list: la liste de toutes les appels d'offres.
    :ivar train_set: le training set qui représente 75 % du corpus total.
    :ivar test_set: le testing set qui représente 25 % du corpus total.
    :ivar vec: l'objet Vectorizer qui permet de construire la matrice items_tags (fréquences TFIDF) à partir du training set.
    :ivar nmf_object: l'objet qui permet de construire la matrice tags_topics grâce à la méthode NMF (Non Negative Matrix Factorization).
    :ivar items_tags: la matrice qui contient la représentation en sacs de mots (bags of words) des appels d'offres du training set.
    :ivar tags_topics: la matrice qui contient les coefficients des topics.
    :ivar clients_topics: la matrice qui contient les topics qui reflètent les profils de chaque client.
    :ivar reco_df: la pandas.DataFrame qui contient résumé des affinités des clients avec chaque nouvel appel d'offres arrivant.
    '''
    class __Singleton:
        
        def __init__(self):
            '''
            Constructor
            '''
            self.THRESHOLD = .85  # Seuil pour accepter/rejetter la recommandation d'un appel d'offres
            
            self.db = db_entity.DB_entity()
            
            self.min_df = 1
            self.max_df = 0.8
            self.n_feature = None
            self.n_components = 500
           
            self.client_list = None
            self.attributed_announce_list = None
            self.unattributed_announce_list = None
            self.announce_list = None
            
            self.train_set = None
            self.test_set = None
            
            if(os.path.isfile(config.VEC_RECO)):
                self.vec = joblib.load(config.VEC_RECO)
            else:
                self.vec = TfidfVectorizer(analyzer=Analyzer(),
                                           max_features=self.n_feature,
                                           min_df=self.min_df,
                                           max_df=self.max_df)

            self.nmf_object = decomposition.NMF(n_components=self.n_components)

            if(os.path.isfile(config.ITEMS_TAGS)):
                self.items_tags = joblib.load(config.ITEMS_TAGS)
            else:
                self.items_tags = None
            
            self.tags_topics = None
            self.clients_topics = None
            self.reco_df = None
        
        def split_train_test(self):
            '''
            Sépare les appels d'offres en deux ensembles :
            - le training set (75%)
            - le test set (25%).
            Cette méthode créer également un training set et un test
            pour chaque client.
            '''
            if os.path.isfile(config.TRAIN_SET) and os.path.isfile(config.TEST_SET):
                self.train_set = joblib.load(config.TRAIN_SET)
                self.test_set = joblib.load(config.TEST_SET)
            else:
                self.attributed_announce_list = self.db.getAnnounceAttributed()
                self.unattributed_announce_list = self.db.getAnnounceAttributed()

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
            Génère la matrice items_tags à partir du 'training set'
            '''
            print("Construction de item_tags")
            if(os.path.isfile(config.ITEMS_TAGS)):
                print("--> début de chargement de item_tags")
                self.items_tags = joblib.load(config.ITEMS_TAGS)
                print("--> fin de chargement de item_tags")
            else:
                print("--> début de génération de item_tags")
                train_set_description = [a['description'] for a in self.train_set]
                self.items_tags = self.vec.fit_transform(train_set_description)
                # sauvegarde du vectorizer avec son vocabulaire 
                joblib.dump(self.vec, config.VEC_RECO)
                joblib.dump(self.items_tags, config.ITEMS_TAGS)
                print("--> fin de génération de item_tags")
        
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
                    client_topics = a_client.get_topics()
                    self.clients_topics.append(client_topics)
                
                joblib.dump(self.clients_topics, config.CLIENTS_TOPICS)
        
        def get_item_clients(self, item):
            '''
            Génère les affinités des clients vis à vis d'un appel d'offres entrant
            '''
            item.get_tags()
            item_topics = sparse.csr_matrix(np.array(item.get_topics()))

            self.get_clients_topics()
            clients_topics = sparse.csr_matrix(np.array(self.clients_topics))

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
        
        
    instance = None
    def __new__(cls):
        if RecoSystem.instance is None:
            RecoSystem.instance = RecoSystem.__Singleton()
        return RecoSystem.instance

    def __getattr__(self, attr):
        return getattr(self.instance, attr)
  
    def __setattr__(self, attr, val):
        return setattr(self.instance, attr, val)
