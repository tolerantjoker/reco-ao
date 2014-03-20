# -*- coding: UTF-8 -*-
'''
Created on 19 mars 2014

@author: tolerantjoker
'''
import db_entity
import client

from preprocessor import Preprocessor

if __name__ == '__main__':
    db = db_entity.DB_entity()
    
    # Création d'une liste de clients
    client_list = db.getClientList()
    #print(client_list)
    clients = []
    for t in client_list:
        c = client.Client(t['id'], t['name'], t['url'])
        clients.append(c)
    # Récupération des données de chaque client
    historic = [(c.id, c.get_historic()) for c in clients]
    #print(historic)
    
    import nltk
    announce_list = db.getAnnounceList()
#     html = announce_list[0]['description']
#     raw = Preprocessor.clean_html(html)
#     print(raw)
#     tokens = Preprocessor.tokenize(raw)
#     print(tokens)
#     print(len(tokens))
#     tokens = Preprocessor.clean_stop_words(tokens)
#     print(tokens)
#     print(len(tokens))
#       
#     print(Preprocessor.normalize(tokens))
    
    html = [a['description'] for a in announce_list]
    print(html)
    from sklearn.feature_extraction.text import CountVectorizer
    vec = CountVectorizer(tokenizer=Preprocessor())
    print(vec)
    data = vec.fit_transform(html).toarray()
    print(data)
     
    vocab = vec.get_feature_names()
    print(len(vocab))
    import numpy as np
    np.clip(data, 0, 1, out=data)
    dist = np.sum(data, axis=0)
    print(dist)
     
    for tag, count in zip(vocab, dist):
        print(count, tag)