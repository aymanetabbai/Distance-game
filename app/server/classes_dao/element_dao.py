from utils.singleton import Singleton
from app.server.classes_dao.configuration import DBConnection

from app.classes_objet.abstract_element import AbstractElement
from app.classes_objet.carte import Carte
from app.classes_objet.equipement import Equipement
from app.classes_objet.monstre import Monstre
from app.classes_objet.de import De

class ElementDAO(metaclass=Singleton) :
    
    def creer(self, element : AbstractElement) -> AbstractElement :
        position = element.position
        id_coordonnees = position.id_coordonnees
        id_api = element.id_api
        est_revele = element.est_revele
        if isinstance(element, Monstre) :
            type_element = 'MONSTRE'
            hp_monstre = element.hp
        else : 
            type_element = 'EQUIPEMENT'
            hp_monstre = 'NULL'
        with DBConnection().connection as connection :
            with connection.cursor() as cursor :
                sql = """INSERT INTO element VALUES
                    (DEFAULT, {}, '{}', '{}', '{}', {}) RETURNING id_element;""".format(id_coordonnees, id_api, est_revele, type_element, hp_monstre)
                cursor.execute(sql)
                id_element = cursor.fetchone()["id_element"]
            connection.commit()
        element.id_element = id_element
        return element
    
    def creer_carte_element(self, carte : Carte, element : AbstractElement) -> None : 
        id_carte = carte.id_carte
        id_element = element.id_element
        # cree une ligne dans la table d'association carte_element
        with DBConnection().connection as connection : 
            with connection.cursor() as cursor : 
                sql = """INSERT INTO carte_element VALUES
                ({}, {})""".format(id_carte, id_element)
                cursor.execute(sql)
            connection.commit()
    
    def row_to_element(self, row : dict) -> AbstractElement :
        if row['type_element'] == 'MONSTRE' :
            return Monstre(row['id_element'], row['id_coordonnees'], row['id_api'], row['est_revele'], row['hp_monstre'])
        else : 
            return Equipement(row['id_element'], row['id_coordonnees'], row['id_api'], row['est_revele'])
        
    def lire(self, id_element : int) -> AbstractElement :
        with DBConnection().connection as connection :
            with connection.cursor() as cursor :
                sql = """SELECT * FROM element WHERE id_element = {}""".format(id_element)
                cursor.execute(sql)
                res = cursor.fetchone()
            connection.commit()
        element = self.row_to_element(res)
        # on a que l'id des coordonnees en sortie
        return element
    
    def creer_monstre_de(self, monstre : Monstre, de : De) -> None :
        id_monstre = monstre.id_element
        id_de = de.id_de
        with DBConnection().connection as connection : 
            with connection.cursor() as cursor : 
                sql = """INSERT INTO monstre_de VALUES
                ({}, {})""".format(id_monstre, id_de)
                cursor.execute(sql)
            connection.commit()
            
    def get_monstre_for_de(self, de : De) -> Monstre : 
        id_de = de.id_de
        with DBConnection().connection as connection :
            with connection.cursor() as cursor :
                sql = """SELECT id_monstre FROM lances_des_acteur_monstre WHERE id_de = {}""".format(id_de)
                cursor.execute(sql)
                res = cursor.fetchone()
            connection.commit()
        monstre = self.lire(res['id_monstre'])
        return monstre
    
    def update(self, element : AbstractElement) -> None :
        id_element = element.id_element
        position = element.position
        id_coordonnees = position.id_coordonnees
        est_revele = element.est_revele
        if isinstance(element, Monstre) :
            hp_monstre = element.hp
        else : 
            hp_monstre = 'NULL'
        with DBConnection().connection as connection :
            with connection.cursor() as cursor :
                sql = """UPDATE element SET
                    id_coordonnees = {}, est_revele = {}, hp_monstre = {}
                    WHERE id_element = {}""".format(id_coordonnees, est_revele, hp_monstre, id_element)
                cursor.execute(sql)
            connection.commit()

    def delete(self, element: AbstractElement) -> None :
        id_element = element.id_element
        with DBConnection().connection as connection :
            with connection.cursor() as cursor :
                sql = """DELETE FROM element WHERE id_element={}""".format(id_element)
                cursor.execute(sql)
            connection.commit()