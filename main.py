# -*- coding: UTF-8 -*-
'''
Created on 19 mars 2014

@author: tolerantjoker
'''
import client
import db_entity
import reco_system

if __name__ == '__main__':
    db = db_entity.DB_entity()
    print("Construction du système de recommandation")
    reco_sys = reco_system.RecoSystem()
    
    print("Construction du training set et du test set")
    reco_sys.split_train_test()
#     print("Construction de items_tags")
#     reco_sys.get_items_tags()
    print("Construction de tags_topics")
    reco_sys.get_tags_topics()
    # print(reco_sys.tags_topics.components_)

#     reco_sys.get_clients_topics()
#     print(len(reco_sys.clients_topics))
#     print(len(reco_sys.clients_topics[0]))
    
    
    # Recommandation d'un appel d'offre à un client
    print("Recommandation d'un appel d'offre à un client")
#     # an_item = reco_sys.test_set[1]
#     for an_item in reco_sys.test_set:
#         # print(an_item)
#         an_item = announce.Announce(an_item)
#         # print(announce)
#         item, item_clients = reco_sys.get_item_clients(an_item)
#         print(item.id)
#         print(item_clients)
    reco_sys.get_clients_topics()
#     print(len(reco_sys.clients_topics))
#     print(reco_sys.clients_topics)

    params = {"id":1245, "name":"company", "url":"http://perdu.com"}
    c = client.Client(params)
     
    df = reco_sys.get_reco_df()
#     print(df[2525988])
    print(df)
#     print(df.loc[c.id])
    
    c.get_reco_series()
    print(c.reco_series)
