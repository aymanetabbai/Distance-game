from typing import List

from app.server.classes_dao.configuration import DBConnection
from utils.singleton import Singleton

from app.classes_objet.coordonnees import Coordonnees
from app.classes_objet.equipement import Equipement
from app.classes_objet.joueur import Joueur
from app.classes_objet.personnage import Personnage

class PersonnageDAO(metaclass=Singleton) :
    
    def creer(self, personnage : Personnage) -> Personnage :
        id_joueur = personnage.joueur.id_acteur
        id_coordonnees = personnage.position.id_coordonnees
        nom = personnage.nom_personnage
        id_api_classe = personnage.id_api_classe
        id_api_race = personnage.id_api_race
        niveau = personnage.niveau
        hp = personnage.hp
        attaque = personnage.attaque
        defense = personnage.defense
        vitesse = personnage.vitesse
        with DBConnection().connection as connection :
            with connection.cursor() as cursor :
                sql = """INSERT INTO personnage VALUES
                    (DEFAULT, {}, {}, '{}', '{}', '{}', {}, {}, {}, {}, {})
                    RETURNING id_personnage;""".format(id_joueur, id_coordonnees, nom, id_api_race, id_api_classe, hp, attaque, defense, vitesse, niveau)
                cursor.execute(sql)
                id_personnage = cursor.fetchone()["id_personnage"]
            connection.commit()
        personnage.id_personnage = id_personnage
        return personnage
    
    def creer_personnage_equipement(self, personnage : Personnage, equipement : Equipement) -> None :
        id_personnage = personnage.id_personnage
        id_equipement = equipement.id_element
        # cree une ligne dans la table d'association personnage_equipement
        with DBConnection().connection as connection : 
            with connection.cursor() as cursor : 
                sql = """INSERT INTO personnage_equipement VALUES
                ({}, {})""".format(id_personnage, id_equipement)
                cursor.execute(sql)
            connection.commit()
        # ne retourne rien
    
    def get_equipements_for_personnage(self, personnage : Personnage) -> List[Equipement] :
        equipements : List[Equipement] = []
        id_personnage = personnage.id_personnage
        with DBConnection().connection as connection : 
            with connection.cursor() as cursor :
                sql = """SELECT * FROM element WHERE id_element IN
                (SELECT id_equipement FROM personnage_equipement WHERE id_personnage = {})""".format(id_personnage)
                cursor.execute(sql)
                res = cursor.fetchall()
            connection.commit()
            for row in res :
                coordonnees = Coordonnees(row['id_coordonnees'], None, None)
                # que l'id des coordonnees
                equipement = Equipement(row['id_element'], coordonnees, row['id_api'], row['est_revele'])
                equipements.append(equipement)
        return equipements
    
    def lire(self, id_personnage : int) -> Personnage : 
        with DBConnection().connection as connection :
            with connection.cursor() as cursor : 
                sql = """SELECT * FROM personnage WHERE id_personnage = {}""".format(id_personnage)
                cursor.execute(sql)
                res = cursor.fetchone()
            connection.commit()
        coordonnees = Coordonnees(res['id_coordonnees'], None, None)
        joueur = Joueur(res['id_acteur'], None, None)
        personnage = Personnage(id_personnage, joueur, coordonnees, res['nom_personnage'], res['id_api_race'],
                                res['id_api_classe'], res['hp'], res['attaque'], res['defense'], res['vitesse'],
                                res['niveau'])
        personnage.equipements = self.get_equipements_for_personnage(personnage)
        return personnage
        
    def get_personnage_for_joueur(self, joueur : Joueur) -> Personnage :
        id_joueur = joueur.id_acteur
        with DBConnection().connection as connection : 
            with connection.cursor() as cursor : 
                sql = """SELECT id_personnage FROM personnage WHERE id_acteur = {}""".format(id_joueur)
                cursor.execute(sql)
                res = cursor.fetchone()
            connection.commit()
        personnage = self.lire(res['id_personnage'])
        # on set le joueur du personnage
        personnage.joueur = joueur
        return personnage
    
    def update(self, personnage : Personnage) -> None :
        # il ne s'agit jamais de changer de joueur, de classe ou de race
        id_personnage = personnage.id_personnage
        id_coordonnees = personnage.position.id_coordonnees
        nom = personnage.nom_personnage
        hp = personnage.hp
        attaque = personnage.attaque
        defense = personnage.defense
        vitesse = personnage.vitesse
        niveau = personnage.niveau
        with DBConnection().connection as connection :
            with connection.cursor() as cursor :
                sql = """UPDATE personnage SET id_coordonnees = {}, nom_personnage = '{}', hp = {},
                attaque = {}, defense = {}, vitesse = {}, niveau = {}
                WHERE id_personnage = {}""".format(id_coordonnees, nom, hp, attaque, defense, vitesse, niveau, id_personnage)
                cursor.execute(sql)
            connection.commit()

    def delete(self, personnage: Personnage) -> None :
        id_personnage = personnage.id_personnage
        with DBConnection().connection as connection :
            with connection.cursor() as cursor :
                sql = """DELETE FROM personnage WHERE id_personnage={}""".format(id_personnage)
                cursor.execute(sql)
            connection.commit()