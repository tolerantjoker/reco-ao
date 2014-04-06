# -*- coding: UTF-8 -*-
'''
Created on 19 mars 2014

@author: tolerantjoker
'''
import client
import db_entity
import reco_system

if __name__ == '__main__':
    
    # On construit un objet base de donnée
    db = db_entity.DB_entity()
    
    # On récupère la liste des clients que l'on passe dans des objets
    client_list = db.getClientList()
    clients = []
    for d in client_list:
        clients.append(client.Client(params=d))
    
    print("Construction du système de recommandation")
    reco_sys = reco_system.RecoSystem()
    
    print("Construction du training set et du test set")
    reco_sys.split_train_test()

    print("Construction de tags_topics")
    reco_sys.get_tags_topics()

    # Recommandation d'un appel d'offre à un client
    print("Recommandation...")
    
    # On récupère le DataFrame
    df = reco_sys.get_reco_df()
#     print(df)
    for c in clients:
#         c.get_reco_series()
        print(c)
#         print(c.reco_series)
        print(c.get_reco_list())
        print('''Appels d'offres déjà recommandés "manuellement" (true positives) : ''' + str(c.tp()))
        print('''Appels d'offres recommandés par notre algorithme mais pas "manuellement" par Jurismarchés (false positives)" : ''' + str(c.fp()))
        print('''Appels d'offres recommandés manuellement par Jurismarchés mais pas par notre algorithme (false negatives) : ''' + str(c.fn()))
        print('PRECISION/RECALL = ' + str(c.precision_recall()))
        print('')

    print(reco_sys.precision_recall())
