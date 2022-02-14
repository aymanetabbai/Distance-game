from typing import List

from app.server.classes_dao.configuration import DBConnection
from utils.singleton import Singleton

from app.classes_objet.abstract_element import AbstractElement
from app.classes_objet.campagne import Campagne
from app.classes_objet.carte import Carte
from app.classes_objet.coordonnees import Coordonnees
from app.classes_objet.equipement import Equipement
from app.classes_objet.monstre import Monstre

class CarteDAO(metaclass=Singleton) :
    
    def creer(self, carte : Carte) -> Carte :
        # cree la carte dans la table carte
        nom = carte.nom_carte
        # verifier que ca rentre bien le booleen ici
        est_actuelle = carte.est_actuelle
        taille = carte.taille
        id_taille = taille.id_coordonnees
        with DBConnection().connection as connection :
            with connection.cursor() as cursor :
                sql = """INSERT INTO carte VALUES (DEFAULT, '{}', {}, '{}')
                RETURNING id_carte""".format(nom, id_taille, est_actuelle)
                cursor.execute(sql)
                res = cursor.fetchone()
            connection.commit()
        carte.id_carte = res["id_carte"]
        return carte

    def creer_campagne_carte(self, campagne : Campagne, carte : Carte) -> None :
        # cree la relation campagne-carte dans la table d'association campagne_carte
        id_campagne = campagne.id_campagne
        id_carte = carte.id_carte
        with DBConnection().connection as connection : 
            with connection.cursor() as cursor : 
                sql = """INSERT INTO campagne_carte VALUES
                ({}, {})""".format(id_campagne, id_carte)
                cursor.execute(sql)
            connection.commit()
        # ne retourne rien

    def row_to_element(self, row : dict) -> AbstractElement :
        # permet de passer a une ligne de sortie de requete a un element
        position = Coordonnees(row['id_coordonnees'], None, None)
        # on a que l'id des coordonnees
        if row['type_element'] == 'MONSTRE' :
            return Monstre(row['id_element'], position, row['id_api'], row['est_revele'], row['hp_monstre'])
        else : 
            return Equipement(row['id_element'], position, row['id_api'], row['est_revele'])
        
    def get_elements_for_carte(self, carte : Carte) -> List[AbstractElement] :
        # recupere tous les elements d'une carte
        elements = []
        id_carte = carte.id_carte
        with DBConnection().connection as connection : 
            with connection.cursor() as cursor :
                sql = """SELECT * FROM element WHERE id_element IN
                (SELECT id_element FROM carte_element WHERE id_carte = {})""".format(id_carte)
                cursor.execute(sql)
                res = cursor.fetchall()
            connection.commit()
        for row in res :
            element = self.row_to_element(row)
            elements.append(element)
        # on a que l'id des coordonnees ici
        return elements
    
    def lire(self, id_carte : int) -> Carte :
        # lit la ligne de la table carte correspondante a l'id rentre
        # pas vraiment utile en soi (on s'en sert jamais je crois)
        with DBConnection().connection as connection :
            with connection.cursor() as cursor :
                sql = """SELECT * FROM carte WHERE id_carte = {}""".format(id_carte)
                cursor.execute(sql)
                res = cursor.fetchone()
            connection.commit()
        nom_carte = res["nom_carte"]
        id_coordonnees = res["id_coordonnees"]
        # a tester avec juste res["est_actuelle"]
        est_actuelle = res["est_actuelle"]
        # on a que l'id des coordonnees de la carte
        coordonnees = Coordonnees(id_coordonnees, None, None)
        carte = Carte(id_carte, nom_carte, coordonnees, est_actuelle)
        # pareil pour les elements on a que l'id de leurs coordonnees
        elements = self.get_elements_for_carte(carte)
        carte.elements = elements
        return carte

    def update(self, carte : Carte) -> None :
        # met a jour la carte
        # ne met pas a jour les elements
        id_carte = carte.id_carte
        nom = carte.nom_carte
        id_coordonnee = carte.taille.id_coordonnees
        est_actuelle = carte.est_actuelle
        with DBConnection().connection as connection :
            with connection.cursor() as cursor :
                sql = """UPDATE carte SET nom_carte = '{}', id_coordonnees = {}, est_actuelle = {}
                WHERE id_carte = {}""".format(nom, id_coordonnee, est_actuelle, id_carte)
                cursor.execute(sql)
            connection.commit()

    def delete(self, carte: Carte) -> None :
        # supprime la carte
        # ne supprime pas les elements lies a la carte
        # askip si du coup
        id_carte = carte.id_carte
        with DBConnection().connection as connection :
            with connection.cursor() as cursor :
                sql = """DELETE FROM carte WHERE id_carte={}""".format(id_carte)
                cursor.execute(sql)
            connection.commit()
  
# --------------------------------------------------------------------------------------------------

#     def get_cartes_de_campagne(self, campagne : Campagne) -> list :
#         cartes = []
#         with DBConnection().connection as connection:
#             with connection.cursor() as cursor:
#                 id_campagne = campagne.id_campagne
#                 sql = """SELECT id_carte FROM carte WHERE id_campagne = {}""".format(id_campagne)
#                 cursor.execute(sql)
#                 res = cursor.fetchall()
#                 for ligne in res:
#                     id_carte = ligne["id_carte"]
#                     carte = self.lire(id_carte)
#                     # on set l'objet campagne ici ?
#                     carte.campagne = campagne
#                     # on a pas les coordonnees par contre
#                     cartes.append(carte)
#         return cartes
    
# # ------------------------------------------------------------------------------------
            
#     def get_elements(self) :
#         # consulter les éléments d'une carte (joueurs : révélés, MJ : tous)
#         # récupération d'une ligne dans la table Carte
#         # + use EquipementDAO, MonstreDAO, PersonnageDAO
#         # ne sert à rien ?
#         pass