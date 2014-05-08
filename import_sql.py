# -*-coding: UTF-8 -*-
'''
Created on 14 mars 2014

:author: François Royer & Valentin Lhommeau
'''
# # Import des appels d'offres
from lxml import etree
import oursql

tree = etree.parse("announces.xml")
announces = tree.xpath("//announce")
announces_params = []
for announce in announces:
    announce_id = announce.xpath("@id")
    announce_title = announce.xpath("title/text()")
    announce_description = announce.xpath("description/text()")
    announce_country = announce.xpath("country/text()")
    if(announce_country == []):
        announces_params.append((announce_id[0], announce_title[0], announce_description[0], ''))
    else:
        announces_params.append((announce_id[0], announce_title[0], announce_description[0], announce_country[0]))
 
# Establishing a connection
conn = oursql.connect(host='localhost', user='root', passwd='', db='test')
    
# Using cursors
query = '''INSERT INTO announces (id, title, description, country) VALUES(?,?,?,?)'''
# params = zip(l_id, l_title, l_description, l_country)
# query = '''DELETE FROM announces'''
with conn.cursor(oursql.DictCursor) as cursor:
    cursor.executemany(query, announces_params)

# # Import des profils clients et des appels d'offres qui leur ont été transmis

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
    
conn = oursql.connect(host='localhost', user='root', passwd='', db='test')
query = '''INSERT INTO companies (id, name, url) VALUES(?,?,?)'''
query2 = '''INSERT INTO assignments (company, announce) VALUES(?,?)'''
with conn.cursor(oursql.DictCursor) as cursor:
    cursor.executemany(query, profiles_params)
    cursor.executemany(query2, assignments)



