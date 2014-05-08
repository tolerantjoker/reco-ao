# -*- coding: UTF-8 -*-
'''
Created on 23 mars 2014

:author: François Royer & Valentin Lhommeau
'''

import reco_system

class Announce(object):
    '''
    Classe qui représente un appel d'offres.
    
    :ivar id: identifiant de l'appel d'offres.
    :ivar title: titre de l'appel d'offres.
    :ivar description: description de l'appel d'offres.
    
    :ivar vec: objet Vectorizer qui créer un BagOfWords d'un appel d'offres.
    :ivar item_tags: matrice qui représente le "BagOfWords model" d'un appel d'offres.
    :ivar item_topics: matrice qui représente les affinités avec les topics d'un appel d'offres.
    :ivar reco_sys: instance du système de recommandation.
    '''

    def __init__(self, params):
        '''
        :param params: un dictionnaire sous la forme : 
        {'id': <id_annonce>,
        'title': <titre_annonce>,
        'description': <description_annonce>}
        '''
        self.id = params['id']
        self.title = params['title']
        self.description = params['description']
    
        self.reco_sys = reco_system.RecoSystem()
        self.item_tags = None
        self.item_topics = None
        
        self.vec = self.reco_sys.vec
        
    def get_tags(self):
        '''
        :return: le vecteur item-tags de l'appel d'offres avec les fréquences tfidf.
        '''
        self.item_tags = self.vec.transform([self.title + self.description])
        return self.item_tags
    
    def get_topics(self):
        '''
        :return: le vecteur item-topics de l'appel d'offres avec ses affinités vis-à-vis de chacun des topics.
        '''
        self.item_topics = self.reco_sys.nmf_object.transform(self.item_tags)
        return self.item_topics
