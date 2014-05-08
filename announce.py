# -*- coding: UTF-8 -*-
'''
Created on 23 mars 2014

:author: François Royer & Valentin Lhommeau
'''

import reco_system

class Announce(object):
    '''
    Classe qui représente un appel d'offre.
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
        Génère le vecteur item-tags de l'appel d'offre
        '''
        self.item_tags = self.vec.transform([self.title + self.description])
        return self.item_tags
    
    def get_topics(self):
        '''
        Détermine les affinités de l'appel d'offre avec les différents topics.
        On calcule les affinités par un calcul de similarité entre item-tags et tags-topics.
        '''
        self.item_topics = self.reco_sys.nmf_object.transform(self.item_tags)
        return self.item_topics
