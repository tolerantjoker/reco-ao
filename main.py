# -*- coding: UTF-8 -*-
'''
Created on 19 mars 2014

@author: tolerantjoker
'''
import db_entity
import client

if __name__ == '__main__':
    db = db_entity.DB_entity()
    
    # Création d'une liste de clients
    client_list = db.getClientList()
    print(client_list)
    clients = []
    for t in client_list:
        c = client.Client(t['id'], t['name'], t['url'])
        clients.append(c)
    # Récupération des données de chaque client    
    historic = [(c.id, c.get_historic()) for c in clients]
    print(historic)