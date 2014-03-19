#-*- coding: UTF-8 -*-
'''
Created on 19 mars 2014

@author: tolerantjoker
'''

import db_entity

class Client(object):
    '''
    classdocs
    '''

    def __init__(self, id, name, url):
        '''
        Constructor
        '''
        self.dbentity = db_entity.DB_entity()
        self.id = id
        self.name = name
        self.url = url
    
    def get_historic(self):
        with self.dbentity.conn.cursor() as cursor:
            query ='''SELECT announce FROM assignments WHERE company = ?'''
            params = (self.id,)
            print(params)
            cursor.execute(query, params)
            return cursor.fetchall()
        
    def get_tags(self):
        pass
    
    def get_topics(self):
        pass