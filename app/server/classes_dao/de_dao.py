from typing import List

from app.server.classes_dao.configuration import DBConnection
from utils.singleton import Singleton

from app.classes_objet.de import De
from app.classes_objet.abstract_acteur import AbstractActeur
from app.classes_objet.monstre import Monstre

class DeDAO(metaclass=Singleton) : 
    
    def creer (self, de : De) -> De :
        max_de = de.max_de
        valeur_de = de.valeur_de
        est_revele = de.est_revele
        est_traite = de.est_traite
        with DBConnection().connection as connection :
            with connection.cursor() as cursor :
                with connection.cursor() as cursor :
                    sql = """INSERT INTO de VALUES
                        (DEFAULT, {}, {}, {}, {}) RETURNING id_de;""".format(max_de, valeur_de, est_revele, est_traite)
                    cursor.execute(sql)
                    id_de = cursor.fetchone()["id_de"]
            connection.commit()
        de = De(id_de, max_de, valeur_de, est_revele, est_traite)
        return de

    def lire(self, id_de : int) -> De :
        with DBConnection().connection as connection :
            with connection.cursor() as cursor :
                sql = """SELECT * FROM de WHERE id_de = {}""".format(id_de)
                cursor.execute(sql)
                res = cursor.fetchone()
            connection.commit()
        max_de = res["max_de"]
        valeur_de = res["valeur_de"]
        est_revele = res["est_revele"]
        est_traite = res["est_traite"]
        return De(id_de, max_de, valeur_de, est_revele, est_traite)

    def update(self, de : De) :
        id_de = de.id_de
        max_de = de.max_de
        valeur_de = de.valeur_de
        est_revele = de.est_revele
        est_traite = de.est_traite
        with DBConnection().connection as connection :
            with connection.cursor() as cursor :
                sql = """UPDATE de SET max_de = {}, valeur_de = {}, est_revele = {}, est_traite = {} WHERE id_de = {}""".format(max_de, valeur_de, est_revele, est_traite, id_de)
                cursor.execute(sql)
            connection.commit()

    def delete(self, de: De) :
        id_de = de.id_de
        with DBConnection().connection as connection :
            with connection.cursor() as cursor :
                sql = """DELETE FROM de WHERE id_de={}""".format(id_de)
                cursor.execute(sql)
            connection.commit()
            
    def creer_de_acteur_monstre(self, de : De, acteur : AbstractActeur, monstre : Monstre) -> None : 
        id_de = de.id_de
        id_acteur = acteur.id_acteur
        id_monstre = monstre.id_element
        with DBConnection().connection as connection :
            with connection.cursor() as cursor :
                sql = """INSERT INTO lances_des_acteur_monstre VALUES
                    ({}, {}, {}, 'NULL')""".format(id_de, id_acteur, id_monstre)
                cursor.execute(sql)
            connection.commit()
        # ne retourne rien
        
    def lire_de_acteur_monstre(self, de : De, acteur : AbstractActeur, monstre : Monstre) -> str : 
        id_de = de.id_de
        id_acteur = acteur.id_acteur
        id_monstre = monstre.id_element
        with DBConnection().connection as connection :
            with connection.cursor() as cursor :
                sql = """SELECT a_gagne FROM lances_des_acteur_monstre WHERE
                    id_de = {}""".format(id_de)
                cursor.execute(sql)
                res = cursor.fetchone()
            connection.commit()
        return res['a_gagne']
        
    def update_de_acteur_monstre(self, de : De, acteur : AbstractActeur, monstre : Monstre, a_gagne : str) -> None :
        id_de = de.id_de
        id_acteur = acteur.id_acteur
        id_monstre = monstre.id_element  
        with DBConnection().connection as connection :
            with connection.cursor() as cursor :
                sql = """UPDATE lances_des_acteur_monstre SET
                    a_gagne = '{}' WHERE
                    id_de = {}""".format(a_gagne, id_de)
                cursor.execute(sql)
            connection.commit()
        
    # def get_des_by_acteur_monstre(self, acteur : AbstractActeur, monstre : Monstre) -> List[De] :
    #     with DBConnection().connection as connection :
    #         with connection.cursor() as cursor :
    #             sql = """SELECT * FROM de WHERE id_de = {}""".format(id_de)
    #             cursor.execute(sql)
    #             res = cursor.fetchone()
    #         connection.commit()
            
    # def get_des_non_traites(self) -> List[De] :
    #     des = []
    #     with DBConnection().connection as connection :
    #         with connection.cursor() as cursor :
    #             sql = """SELECT id_de FROM de WHERE est_traite = false"""
    #             cursor.execute(sql)
    #             res = cursor.fetchall()
    #         connection.commit()
    #     for row in res : 
    #         de = self.lire(row['id_de'])
    #         des.append(de)
    #     return des