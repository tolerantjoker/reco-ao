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
            '''
            Retourne la liste des clients sous forme d'une liste de dictionnaires.
            Un client : {'id': 48, 'name': 'ABELIUM COLLECTIVITES', 'url': 'http://www.abelium-collectivites.fr/'}
            '''
            with self.conn.cursor(oursql.DictCursor) as cursor:
                query = '''SELECT * FROM companies'''
                cursor.execute(query)
                return cursor.fetchall()
        
        def getClientAnnounces(self, id_client):
            '''
            Retourne la liste des appels d'offres envoyés au client numéro 'id_client'.
            Un appel d'offre : {
            'id': 28801,
            'title': 'Marché de maitrise d'oeuvre destiné à désigner une équipe d'auteurs 
            de projet pour mener à bien les études et le suivi de l'exécution des travaux 
            de revitalisation et de rénovation du Domaine de Mariemont situé 100, 
            chaussée de Mariemont à 7140 MORLANWELZ.'
            'description' : '<div id="avisDetail"><div id="topFonctions"><a ><img alt="" name="impression" src="http://marchespublics.wallonie.be/img/bouton_imprimer-fr.gif"></a></div><p class="back"><a >&lt;&lt; Retour aux résultats de la recherche</a></p><h3>Intitulé du marché :</h3><p>Marché de maitrise d'oeuvre destiné à désigner une équipe d'auteurs de projet pour mener à bien les études et le suivi de l'exécution des travaux de revitalisation et de rénovation du Domaine de Mariemont situé 100, chaussée de Mariemont à 7140 MORLANWELZ.</p><h3>Date de clôture :</h3><p>30/05/2011</p><h3>Description / objet du marché :</h3><div class="objetMarche"><p>Marché par PROCEDURE NEGOCIEE AVEC PUBLICITE EUROPEENNE destiné à désigner une équipe d auteurs de projet pour mener à bien les études et le suivi des travaux de revitalisation et de rénovation du Domaine de Mariemont situé 100, chaussée de Mariemont à 7140 MORLANWELZ. Le Domaine de Mariemont est un site classé de 44 ha habritant des bâtiments, plantations et oeuvres d'art à tous égards remarquables, dont le Musée de Mariemont. L'équipe auteurs de projet devra donc être pluridisciplinaire afin de pouvoir maitriser toutes les facettes présentées par le site. L'enjeu majeur de ce projet étant de préparer le Musée mais aussi le Domaine à relever les défis de son temps et accroitre les potentiels de ce magnifique site.<br>A cette fin, la mission comportera trois lots :<br>*Lot 1 : réalisation d'un schéma directeur qui abordera de manière globale les questions paysagères et fonctionnelles, et qui proposera un phasage technique et financier. Le lot 1 est commun au Ministère de la Communauté française et au Service public wallon;<br>*Lot 2 : la mission complète d'étude et de suivi des travaux portant sur la revalorisation et la rénovation du Domaine de Mariemont en tenant compte des diverses options développées au terme de l'approbation du LOT 1,portant sur les travaux à charge du Ministère de la Communauté française.<br>*Lot 3 : la mission complète d'architecture et d'architecture du paysage portant sur la revalorisation et restauration du Domaine de Mariemont en tenant compte des diverses options développées au terme de l'approbation du LOT 1, portant sur les travaux à charge du Service public wallon.<br></p></div><h3>Documents liés</h3><p><img align="absmiddle" alt="html" src="http://marchespublics.wallonie.be/img/picto_small_HTML.gif"><a target="_blank" href="http://avis.marchespublics.wallonie.be/avis.marches.publics/servlet/Statistique?redirect=http://avis.marchespublics.wallonie.be/avis.marches.publics/documents/Pam/Avis/100511.html&amp;filename=100511.html">Avis n° 100511</a> (63)</p><h3>Détails de l'avis</h3><table class="detailFin" cellspacing="0"><tr><th>Pouvoir adjudicateur :</th><td>CF_MCF_AGI - Service des Infrastructures culturelles</td></tr><tr><th>Type de marchés : </th><td>Services</td></tr><tr><th>Secteur : </th><td>Classique</td></tr><tr><th>Niveau de publicité :</th><td>Europeen</td></tr><tr><th>Numéro de référence attribué au dossier par le pouvoir adjudicateur :</th><td>CF/SPW/MARIEMONT AP/2011</td></tr><tr><th>Date de mise à disposition de l'avis :</th><td>27/03/2011</td></tr><tr><th>Date limite de réception des offres ou des demandes de participation :</th><td>30/05/2011</td></tr><tr><th>Code CPV :</th><td>[71200000-0] : Services d'architecture, [71420000-8] : Services d'architecture paysagère</td></tr></table><p> </p><p> </p></div>'}
            '''
            with self.conn.cursor(oursql.DictCursor) as cursor:
                query = '''
                            SELECT announces.id, announces.title, announces.description
                            FROM assignments
                            JOIN announces ON assignments.announce = announces.id
                            WHERE company = ?
                        '''
                params = (id_client,)
                cursor.execute(query, params)
                return cursor.fetchall()
        
        def getAnnounceList(self):
            with self.conn.cursor(oursql.DictCursor) as cursor:
                query = '''SELECT * FROM announces'''
                cursor.execute(query)
                return cursor.fetchall()
        
        def getAnnounceAttributed(self):
            with self.conn.cursor(oursql.DictCursor) as cursor:
                query = '''SELECT * FROM announces WHERE id IN (SELECT announce FROM assignments)'''
                cursor.execute(query)
                return cursor.fetchall()
            
        def getAnnounceUnattributed(self):
            with self.conn.cursor(oursql.DictCursor) as cursor:
                query = '''SELECT * FROM announces WHERE id NOT IN (SELECT announce FROM assignments)'''
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

            
