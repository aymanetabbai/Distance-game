from typing import List

from utils.singleton import Singleton
from app.server.classes_dao.configuration import DBConnection

from app.classes_objet.monstre import Monstre
from app.classes_objet.campagne import Campagne
from app.classes_objet.joueur import Joueur
from app.classes_objet.utilisateur import Utilisateur
from app.classes_objet.abstract_acteur import AbstractActeur
from app.classes_objet.maitre_jeu import MaitreJeu
from app.classes_objet.de import De

class ActeurDAO(metaclass=Singleton): 

    def creer(self, acteur : AbstractActeur) -> AbstractActeur :
        # cree un acteur dans la base de donnees
        # est_mj depend de l'instance de l'objet que l'on rentre en argument
        nom_utilisateur = acteur.nom_utilisateur
        if isinstance(acteur, MaitreJeu) :
            est_mj = True
        elif isinstance(acteur, Joueur) :
            est_mj = False
        with DBConnection().connection as connection :
            with connection.cursor() as cursor :
                sql = """INSERT INTO acteur VALUES
                    (DEFAULT, '{}', {}) RETURNING id_acteur""".format(nom_utilisateur, est_mj)
                cursor.execute(sql)
                res = cursor.fetchone()
            connection.commit()
        # on set l'id de l'acteur avec celui que retourne la requete 
        id_acteur = res["id_acteur"]
        acteur.id_acteur = id_acteur
        return acteur

    def creer_campagne_acteur(self, campagne : Campagne, acteur : AbstractActeur) -> None :
        # cree la relation entre une campagne et un acteur
        id_campagne = campagne.id_campagne
        id_acteur = acteur.id_acteur
        with DBConnection().connection as connection : 
            with connection.cursor() as cursor : 
                sql = """INSERT INTO campagne_acteur VALUES
                ({}, {})""".format(id_campagne, id_acteur)
                cursor.execute(sql)
            connection.commit()
        # ne retourne rien
    
    def row_to_acteur(self, row : dict) -> AbstractActeur : 
        # cf CampagneDAO
        if row['est_mj'] : 
            return MaitreJeu(row['id_acteur'], row['username'])
        else :
            return Joueur(row['id_acteur'], row['username'])

    def get_des_for_acteur(self, acteur : AbstractActeur) -> List[De] :
        # retourne les des d'un acteur
        id_acteur = acteur.id_acteur
        des : List[De] = []
        with DBConnection().connection as connection : 
            with connection.cursor() as cursor : 
                sql = '''SELECT * FROM de WHERE id_de IN
                (SELECT id_de FROM lances_des_acteur_monstre WHERE id_acteur = {})'''.format(id_acteur)
                cursor.execute(sql)
                res = cursor.fetchall()
            connection.commit()
        for row in res : 
            de = De(row['id_de'], row['max_de'], row['valeur_de'], row['est_revele'], row['est_traite'])
            des.append(de)
        return des
    
    def lire(self, id_acteur : int) -> AbstractActeur :
        # retour l'acteur associe a l'id
        with DBConnection().connection as connection :
            with connection.cursor() as cursor :
                sql = """SELECT * FROM acteur WHERE id_acteur = {}""".format(id_acteur)
                cursor.execute(sql)
                res = cursor.fetchone()
                acteur = self.row_to_acteur(res)
            connection.commit()
        acteur.lances_des = self.get_des_for_acteur(acteur)
        return acteur
    
    def get_acteurs_for_user(self, utilisateur : Utilisateur) -> List[AbstractActeur] :
        # recupere les acteurs associe a un utilisateur
        nom_utilisateur = utilisateur.nom_utilisateur
        # recupere tous les acteurs qui reference a un utilisateur(REFERENCES username)
        acteurs : List[AbstractActeur] = []
        with DBConnection().connection as connection :
            with connection.cursor() as cursor :
                sql = """SELECT * FROM acteur WHERE username = '{}'""".format(nom_utilisateur)
                cursor.execute(sql)
                res = cursor.fetchall()
            connection.commit()
        for row in res:
            acteur = self.lire(row['id_acteur'])
            acteurs.append(acteur)
        return acteurs
            
    def get_acteur_for_de(self, de : De) -> AbstractActeur : 
        id_de = de.id_de
        with DBConnection().connection as connection :
            with connection.cursor() as cursor :
                sql = """SELECT id_acteur FROM lances_des_acteur_monstre WHERE id_de = {}""".format(id_de)
                cursor.execute(sql)
                res = cursor.fetchone()
            connection.commit()
        acteur = self.lire(res['id_acteur'])
        return acteur
    
    def update(self, acteur : AbstractActeur) -> AbstractActeur :
        id_acteur = acteur.id_acteur
        nom_utilisateur=acteur.nom_utilisateur
        with DBConnection().connection as connection :
            with connection.cursor() as cursor :
                sql = """UPDATE acteur SET username='{}' WHERE id_acteur={} """.format(nom_utilisateur, id_acteur)
                cursor.execute(sql)
            connection.commit()
        return acteur

    def delete(self, acteur: AbstractActeur):
        id_acteur = acteur.id_acteur
        with DBConnection().connection as connection :
            with connection.cursor() as cursor :
                sql = """DELETE FROM acteur WHERE id_acteur={}""".format(id_acteur)
                cursor.execute(sql)
            connection.commit()

