# -*- coding: UTF-8 -*-
'''
Created on 19 mars 2014

@author: tolerantjoker
'''

import oursql

import db_entity
import numpy as np
import reco_system
import os
import config
from sklearn.externals import joblib


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
        
        self.train_set = None
        self.test_set = None
        
        if os.path.isfile(config.CLIENT_TRAIN_SET + str(self.id) + '.save'):
            self.train_set = joblib.load(config.CLIENT_TRAIN_SET + str(self.id) + '.save')
        if os.path.isfile(config.CLIENT_TEST_SET + str(self.id) + '.save'):
            self.test_set = joblib.load(config.CLIENT_TEST_SET + str(self.id) + '.save')
        
        
        self.reco_sys = reco_system.RecoSystem()
        self.historic = None
        self.client_tags = None
        self.client_topics = None
        
#         self.vec = TfidfVectorizer(tokenizer=Preprocessor(),
#                               max_features=self.reco_sys.n_feature,
#                               vocabulary=self.reco_sys.vec.vocabulary_.keys())
#         self.vec = HashingVectorizer(tokenizer=Preprocessor(),
#                                      vocabulary=self.reco_sys.vec.vocabulary_.keys(),
#                                      non_negative=True)
        self.vec = self.reco_sys.vec
        
        self.reco_series = None
        
    def __str__(self):
        return str(self.id) + '\n' + self.name + '\n' + self.url + '\n'
        
    def get_historic(self):
        '''
        Retourne la liste des appels d'offres qui ont été attribués au client.
        '''
#         with self.dbentity.conn.cursor(oursql.DictCursor) as cursor:
#             query = '''
#             SELECT assignments.announce, announces.description
#             FROM assignments
#             JOIN announces ON assignments.announce = announces.id
#             WHERE company = ?'''
#             params = (self.id,)
#             cursor.execute(query, params)
#             historic = cursor.fetchall()
#             announces_train_id = [e['id'] for e in self.reco_sys.train_set]
#             self.historic = [e for e in historic if e['announce'] in announces_train_id]
        self.historic = [a['title'] + a['description'] for a in self.train_set]

        
    def get_tags(self):
        '''
        Renvoie le modèle 'bag-of-words' d'un client.
        Ce modèle est construit à partir de l'historique des appels d'offres du client.
        '''
        self.get_historic()
#         historic = [a['title'] + a['description'] for a in self.historic]
        self.client_tags = self.vec.transform(self.historic)
    
    def get_topics(self):
        '''
        Renvoie les affinités du client avec chaque topic
        '''
        self.get_tags()
        self.client_topics = self.reco_sys.nmf_object.transform(self.client_tags)
#         self.client_topics = cosine_similarity(self.client_tags,
#                                                sparse.csr_matrix(np.array(self.reco_sys.tags_topics.components_)))
        self.client_topics = np.mean(np.asarray(self.client_topics), axis=0)
        return self.client_topics

    def get_reco_series(self):
        '''
        Renvoie la liste des appels d'offres recommandés au client,
        avec pour chaque appel d'offres sa note associé.
        '''
        self.reco_sys.get_reco_df()
        reco_df = self.reco_sys.reco_df
        self.reco_series = reco_df.loc[self.id]
        self.reco_series = self.reco_series[self.reco_series > self.reco_sys.THRESHOLD]
        self.reco_series = self.reco_series.order(ascending=False)
    
    def get_reco_list(self):
        '''
        Renvoie la liste des identifiants des appels d'offres recommandés au client par le RecoSystem.
        '''
        if self.reco_series is None:
            self.get_reco_series()
        return self.reco_series.index.tolist()
    
    def get_list_jurismarches(self):
        '''
        Retourne la liste des appels d'offres que Jurismarchés avait envoyés au client.
        '''
        def get_hist_set_ids():
            with self.dbentity.conn.cursor() as cursor:
                query = '''
                        SELECT announce
                        FROM assignments
                        WHERE assignments.company = ?
                        '''
                params = (self.id,)
                cursor.execute(query, params)
                res = cursor.fetchall()
                res = reduce(list.__add__, map(list, res))
            return set(res)
        def get_test_set_ids():
            return set([a['id'] for a in self.reco_sys.test_set])
          
        return list(get_hist_set_ids() & get_test_set_ids())
#         return [a['id'] for a in self.test_set]
    
    def tp(self):
        '''
        Retourne les 'true positives' c'est-à-dire la liste des appels d'offres que nous avons recommandés
        au client ET qui lui avaient effectivement été recommandés par Jurismarchés.
        '''
        return list(set(self.get_list_jurismarches()) & set(self.get_reco_list()))
    
    def fp(self):
        '''
        Retourne les 'false positives' c'est-à-dire la liste des appels d'offres que nous avons recommandés
        au client MAIS qui ne lui avaient pas été recommandés par Jurismarchés.
        '''
        return list(set(self.get_reco_list()) - set(self.get_list_jurismarches()))
    
    def fn(self):
        '''
        Retourne les 'false negatives' c'est-à-dire la liste des appels d'offres que Jurismarchés lui avait 
        recommandés mais que nous ne lui avons pas recommandés.
        '''
        return list(set(self.get_list_jurismarches()) - set(self.get_reco_list()))
    
    def precision_recall(self):
        '''
        Retourne les valeurs des métriques precision/recall.
        '''
        tp = float(len(self.tp()))
        fp = float(len(self.fp()))
        fn = float(len(self.fn()))
        try:
            return tp / (tp + fp), tp / (tp + fn)
        except ZeroDivisionError:
            return 0.0, 0.0
        
    
    
