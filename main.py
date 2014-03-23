# -*- coding: UTF-8 -*-
'''
Created on 19 mars 2014

@author: tolerantjoker
'''
import client
import announce
import db_entity
import reco_system
from preprocessor import Preprocessor


if __name__ == '__main__':
    db = db_entity.DB_entity()
    reco_sys = reco_system.RecoSystem()
    
    reco_sys.split_train_test()
    reco_sys.get_items_tags()
    reco_sys.get_tags_topics()
    
    # Création d'une liste de clients
    client_list = db.getClientList()
    print(client_list)
    clients = []
    for t in client_list:
        c = client.Client(t)
        clients.append(c)
    print(clients)
    # Récupération des données de chaque client
    
#     for c in clients:
#         historic = c.get_historic()
#         print([h['announce'] for h in historic])
    a_client = clients[0]
    historic = a_client.get_historic()
    print(len(historic))
    client_tags = a_client.get_tags()
    print(len(client_tags))
    clients_topics = a_client.get_topics()
    print(clients_topics)