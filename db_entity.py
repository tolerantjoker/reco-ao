#-*- coding: UTF-8 -*-
'''
Created on 19 mars 2014

@author: tolerantjoker
'''
import oursql
import db_config

class DB_entity(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.conn = oursql.connect(host='localhost', user='root', passwd='', db='test')

    def getClientList(self):
        with self.conn.cursor() as cursor:
            query = "SELECT * FROM companies"
            cursor.execute(query)
            return cursor.fetchall()
    
            