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
    clients = []
    for t in client_list:
        c = client.Client(t[0], t[1], t[2])
        clients.append(c)
    # Récupération des données de chaque client
    for c in clients:
        print(c.get_historic())
