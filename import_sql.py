# -*-coding: UTF-8 -*-
'''
Created on 14 mars 2014

@author: tolerantjoker
'''
## Import des appels d'offres
from lxml import etree
    
tree = etree.parse("announces.xml")
l_id = tree.xpath("//announce/@id")
l_title = tree.xpath("//announce/title/text()")
l_description = tree.xpath("//announce/description/text()")
    
import oursql
# Establishing a connection
conn = oursql.connect(host='localhost', user='root', passwd='', db='test')
    
# Using cursors
query = '''INSERT INTO announces (id, title, description) VALUES(?,?,?)'''
params = zip(l_id, l_title, l_description)
#query = '''DELETE FROM announces'''
with conn.cursor(oursql.DictCursor) as cursor:
    cursor.executemany(query, params)

## Import des profils clients et des appels d'offres qui leur ont été transmis
from lxml import etree

tree = etree.parse("profiles.xml")
profiles = tree.xpath("//company")

profiles_params = []
assignments = []
for profile in profiles:
    profil_id = profile.xpath("@id")
    profil_name = profile.xpath("name/text()")
    profil_url = profile.xpath("url/text()")
    profiles_params.append((profil_id[0], profil_name[0], profil_url[0]))
    relations = profile.xpath("test/announce/@id") + profile.xpath("train/announce/@id")
    assignments.extend([(profil_id[0], x) for x in relations])
    
import oursql
conn = oursql.connect(host='localhost', user='root', passwd='', db='test')
query = '''INSERT INTO companies (id, name, url) VALUES(?,?,?)'''
query2 = '''INSERT INTO assignments (coclientannounce) VALUES(?,?)'''
with conn.cursor(oursql.DictCursor) as cursor:
    cursor.executemany(query, profiles_params)
    cursor.executemany(query2, assignments)



