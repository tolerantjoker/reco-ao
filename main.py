# -*- coding: UTF-8 -*-
'''
Created on 19 mars 2014

@author: tolerantjoker
'''
import numpy as np
import client
import announce
import db_entity
import reco_system
from preprocessor import Preprocessor


if __name__ == '__main__':
    db = db_entity.DB_entity()
    print("Construction du système de recommandation")
    reco_sys = reco_system.RecoSystem()
    
    print("Construction du training set et du test set")
    reco_sys.split_train_test()
    print("Construction de items_tags")
    reco_sys.get_items_tags()
    print("Construction de tags_topics")
    reco_sys.get_tags_topics()
    
#     # Création d'une liste de clients
#     print("Création d'une liste de clients")
#     client_list = db.getClientList()
#     print(client_list)
#     clients = []
#     for t in client_list:
#         c = client.Client(t)
#         clients.append(c)
#     print(clients)
#     # Récupération des données de chaque client
#     print("Récupération des données de chaque client")
    
#     for c in clients:
#         historic = c.get_historic()
#         print([h['announce'] for h in historic])
#     for a_client in clients:
#      a_client = clients[0]
#      historic = a_client.get_historic()
#      print(len(historic))
#      client_tags = a_client.get_tags()
#      print(len(client_tags))
#      client_topics = a_client.get_topics()
#      print(client_topics)

    
#     Recommandation d'un appel d'offre à un client
    print("Recommandation d'un appel d'offre à un client")
    # an_item = reco_sys.test_set[0]
    for an_item in reco_sys.test_set:
        # print(an_item)
        an_item = announce.Announce(an_item)
        # print(announce)
        item, item_clients = reco_sys.get_item_clients(an_item)
        print(item.id)
        print(item_clients)
