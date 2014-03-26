# -*- coding: UTF-8 -*-
'''
Created on 19 mars 2014

@author: tolerantjoker
'''
import oursql
from db_config import db_config

class DB_entity(object):
    '''
    classdocs
    '''
    class __Singleton:
        def __init__(self):
            self.conn = oursql.connect(host=db_config['host'], user=db_config['user'],
                                       passwd=db_config['password'], db=db_config['db'])
            
        def __str__(self):
            return `self`
        
        def getClientList(self):
            with self.conn.cursor(oursql.DictCursor) as cursor:
                query = '''SELECT * FROM companies'''
                cursor.execute(query)
                return cursor.fetchall()
        
        def getAnnounceList(self):
            with self.conn.cursor(oursql.DictCursor) as cursor:
                query = '''SELECT * FROM announces  LIMIT 0,1000'''
                cursor.execute(query)
                return cursor.fetchall()
        
        def getAnnounceAttributed(self):
            with self.conn.cursor(oursql.DictCursor) as cursor:
                query = '''SELECT * FROM announces WHERE id IN (SELECT announce FROM assignments) LIMIT 0,1000'''
                cursor.execute(query)
                return cursor.fetchall()
            
        def getAnnounceUnattributed(self):
            with self.conn.cursor(oursql.DictCursor) as cursor:
                query = '''SELECT * FROM announces WHERE id NOT IN (SELECT announce FROM assignments) LIMIT 0,1000'''
                cursor.execute(query)
                return cursor.fetchall()
    # Instance propre au pattern singleton
    instance = None
    
    def __new__(cls):
        if DB_entity.instance is None:
            DB_entity.instance = DB_entity.__Singleton()
        return DB_entity.instance

    def __getattr__(self, attr):
        return getattr(self.instance, attr)
  
    def __setattr__(self, attr, val):
        return setattr(self.instance, attr, val)

            
