from app.server.classes_dao.configuration import DBConnection
from utils.singleton import Singleton

from app.classes_objet.coordonnees import Coordonnees

class CoordonneesDAO(metaclass=Singleton) :
    
    def creer(self, coordonnees : Coordonnees) -> Coordonnees :
        """
        Créer une ligne dans la table coordonnees. Renvoie l'id de la position.
        """
        x = coordonnees.coordonnee_x
        y = coordonnees.coordonnee_y
        with DBConnection().connection as connection :
            with connection.cursor() as cursor :
                sql = """INSERT INTO coordonnees VALUES (DEFAULT, {}, {}) RETURNING id_coordonnees;""".format(x,y)
                cursor.execute(sql)
                id_coordonnees = cursor.fetchone()["id_coordonnees"]
            connection.commit()
        coordonnees = Coordonnees(id_coordonnees, x, y)
        return coordonnees
        
    def lire(self, id_coordonnees : int) -> Coordonnees :
        with DBConnection().connection as connection :
            with connection.cursor() as cursor :
                sql = """SELECT * FROM coordonnees WHERE id_coordonnees = {}""".format(id_coordonnees)
                cursor.execute(sql)
                res = cursor.fetchone()
                x = res["coordonnee_x"]
                y = res["coordonnee_y"]
            connection.commit()
        coordonnees = Coordonnees(id_coordonnees, x, y)
        return coordonnees

    def update(self, coordonnees : Coordonnees) -> Coordonnees :
        with DBConnection().connection as connection :
            with connection.cursor() as cursor :
               id_coordonnees = coordonnees.id_coordonnees
               coordonnee_x = coordonnees.coordonnee_x
               coordonnee_y = coordonnees.coordonnee_y
               sql = """UPDATE coordonnees SET coordonnee_x = {}, coordonnee_y = {} WHERE id_coordonnees = {} """.format(coordonnee_x, coordonnee_y, id_coordonnees)
               cursor.execute(sql)
            connection.commit()
        return coordonnees

# ----------------------------------------------------------------------------------------------------

    def consulter(self) :
        # consulter la position d'un élément (Joueurs : révélés, MJ : tous) + consultr la position d'un personnage
        # récupération d'une ligne dans la table Coordonnees
        # ne sert à rien
        pass

    def delete(self, coordonnees: Coordonnees):
        id_coordonnees = coordonnees.id_coordonnees
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                sql = """DELETE FROM coordonnees WHERE id_coordonnees={}""".format(id_coordonnees)
                cursor.execute(sql)
            connection.commit()
            
if __name__ == "__main__" :
     pass