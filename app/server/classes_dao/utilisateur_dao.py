from app.server.classes_dao.configuration import DBConnection
from utils.singleton import Singleton

from app.classes_objet.utilisateur import Utilisateur

class UtilisateurDAO (metaclass=Singleton):
    
    def verifyPassword(self, username: str, password: str) -> bool:
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                sql = """SELECT * FROM utilisateur 
                    WHERE username = '{}' AND mot_de_passe = '{}';""".format(username, password)
                cursor.execute(sql)
                res = cursor.fetchone()
            connection.commit()
        if res is not None:
            return True
        else:
            return False

    def getUser(self, username: str) -> Utilisateur:
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                sql = """SELECT * FROM utilisateur WHERE username = '{}'""".format(username)
                cursor.execute(sql)
                res = cursor.fetchone()
            connection.commit()
        try :
            utilisateur = Utilisateur(nom_utilisateur=res["username"], mot_de_passe=res["mot_de_passe"])
            return utilisateur
        except :
            raise Exception("user not found")

    def createUser(self, user: Utilisateur) -> Utilisateur:
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                username = user.nom_utilisateur
                mot_de_passe = user.mdp
                sql = """INSERT INTO utilisateur VALUES
                    ('{}', '{}', DEFAULT);""".format(username, mot_de_passe)
                cursor.execute(sql)
            connection.commit()
        return UtilisateurDAO.getUser(self, username)

    def updateUser(self, user: Utilisateur) -> None:
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                sql = """UPDATE utilisateur SET mot_de_passe='{}' WHERE username = '{}';""".format(user.mdp, user.nom_utilisateur)
                cursor.execute(sql)
            connection.commit()

    def deleteUser(self, user: Utilisateur) -> None:
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                sql = """DELETE FROM utilisateur WHERE username = '{}';""".format(user.nom_utilisateur)
                cursor.execute(sql)
            connection.commit()