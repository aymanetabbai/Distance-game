from typing import List

from app.server.classes_dao.configuration import DBConnection
from utils.singleton import Singleton

from app.classes_objet.campagne import Campagne
from app.classes_objet.carte import Carte
from app.classes_objet.abstract_acteur import AbstractActeur
from app.classes_objet.coordonnees import Coordonnees
from app.classes_objet.joueur import Joueur
from app.classes_objet.maitre_jeu import MaitreJeu

# on pourrait aussi faire des static method
# relativement equivalent ici

class CampagneDAO(metaclass=Singleton) :
    """Classe qui gére l'enregistrement, la lecture, la modification et la suppression des objets de type Campagne dans la base de données

    Args:
        metaclass (class): Singleton.
    """
    def creer(self, campagne : Campagne) -> Campagne :
        """Crée une ligne dans la table campagne
        PS : on considère que lorsqu'on crée la campagne il n'y a ni cartes ni éléments associés

        Args:
            campagne (Campagne): objet campagne que l'on souhaite créer dans la table
            son id est None car on le récupére automatiquement grâce au séquençage de l'id_camapgne

        Returns:
            Campagne: objet campagne identique avec l'id recupéré suite à la requête SQL
        """
        nom = campagne.nom_campagne
        nb_places_libres = campagne.nb_places_libres
        with DBConnection().connection as connection :
            with connection.cursor() as cursor :
                sql = """INSERT INTO campagne VALUES (DEFAULT, '{}', {}, DEFAULT)
                RETURNING id_campagne""".format(nom, nb_places_libres)
                cursor.execute(sql)
                res = cursor.fetchone()
            connection.commit()
        id_campagne = res["id_campagne"]
        # on renvoie la campagne avec le bon id
        campagne.id_campagne = id_campagne
        return campagne
        
    def get_cartes_for_campagne(self, campagne : Campagne) -> List[Carte] :
        """Retourne les cartes d'une campagne

        Args:
            campagne (Campagne): objet campagne dont on veut récupérer les cartes

        Returns:
            List[Carte]: liste des cartes de la campagne. Attention: on a que l'id des coordonnées
            de la taille de la carte et on a pas la liste des éléments de la carte
        """
        cartes = []
        id_campagne = campagne.id_campagne
        with DBConnection().connection as connection : 
            with connection.cursor() as cursor :
                sql = """SELECT * FROM carte WHERE id_carte IN
                (SELECT id_carte FROM campagne_carte WHERE id_campagne = {})""".format(id_campagne)
                cursor.execute(sql)
                res = cursor.fetchall()
            connection.commit()
        for row in res :
        # on a que l'id des coordonnees
        # on a pas la liste des elements
            coordonnees = Coordonnees(row['id_coordonnees'], None, None)
            carte = Carte(row['id_carte'], row['nom_carte'], coordonnees, row['est_actuelle'])
            cartes.append(carte)
        return cartes
    
    def row_to_acteur(self, row : dict) -> AbstractActeur : 
        """Retourne un acteur à partir d'une ligne de requête relative à la table acteur\n
        Méthode utilisée pour récupérer les acteurs d'une campagne

        Args:
            row (dict): ligne en sortie de requête SQL

        Returns:
            AbstractActeur: acteur correspondant à la ligne lue
        """
        if row['est_mj'] : 
            return MaitreJeu(row['id_acteur'], row['username'])
        else :
            return Joueur(row['id_acteur'], row['username'])

    def get_acteurs_for_campagne(self, campagne : Campagne) -> List[AbstractActeur] :
        """Retourne les acteurs d'une campagne\n
        Méthode qui utilise la méthode row_to_acteur

        Args:
            campagne (Campagne): objet campagne dont on veut récupérer les acteurs

        Returns:
            List[AbstractActeur]: liste des acteurs de la campagne
        """
        acteurs = []
        id_campagne = campagne.id_campagne 
        with DBConnection().connection as connection :
            with connection.cursor() as cursor :
                sql = """SELECT * FROM acteur WHERE id_acteur IN
                (SELECT id_acteur FROM campagne_acteur WHERE id_campagne = {})""".format(id_campagne)
                cursor.execute(sql)
                res = cursor.fetchall()
            connection.commit()
        for row in res :
            # on utilise la methode row_to_acteur ici
            acteur = self.row_to_acteur(row)
            acteurs.append(acteur)
        return acteurs
    
    def lire(self, id_campagne : int) -> Campagne :
        """Lit dans la table campagne la ligne correspondante à l'id rentré et renvoie l'objet campagne correspondant

        Args:
            id_campagne (int): id de la campagne dont on veut récupérer les informations

        Returns:
            Campagne: objet campagne correspondant à l'id rentré
        """ 
        with DBConnection().connection as connection :
            with connection.cursor() as cursor :
                sql = """SELECT nom_campagne, nb_places_libres FROM campagne
                WHERE id_campagne = {}""".format(id_campagne)
                cursor.execute(sql)
                res = cursor.fetchone()
            connection.commit()
        nom = res["nom_campagne"]
        nb_places_libres = res["nb_places_libres"]
        campagne = Campagne(id_campagne, nom, nb_places_libres)
        # grace aux fonctions ci-dessus ont peut set les acteurs et les cartes de la campagne
        campagne.acteurs = self.get_acteurs_for_campagne(campagne)
        campagne.cartes = self.get_cartes_for_campagne(campagne)
        return campagne

    def get_campagnes_pas_pleines(self) -> List[Campagne] :
        """Retourne les campagnes non pleines

        Returns:
            List[Campagne]: liste de toutes les campagnes qui ne sont pas encore pleines
        """
        campagnes = []
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                sql = """SELECT id_campagne FROM campagne WHERE nb_places_libres > 0"""
                cursor.execute(sql)
                res = cursor.fetchall()
            connection.commit()
        for row in res:
            id_campagne = row["id_campagne"]
            campagne = self.lire(id_campagne)
            campagnes.append(campagne)
        # recuperer les id puis les lire permet d'avoir le bon objet avec les acteurs et les elements
        return campagnes

    def get_campagne_for_acteur(self, acteur : AbstractActeur) -> Campagne :
        """Récupère la campagne d'un acteur

        Args:
            acteur (AbstractActeur): acteur dont on veut récupérer la campagne
            
        Returns:
            Campagne: objet correspondant à la campagne de l'acteur
        """
        id_acteur = acteur.id_acteur
        with DBConnection().connection as connection :
            with connection.cursor() as cursor :
                sql = """SELECT id_campagne FROM campagne_acteur WHERE id_acteur = {}""".format(id_acteur)
                cursor.execute(sql)
                res = cursor.fetchone()
            connection.commit()
        # on recupere d'abord l'id puis on lit la campagne pour avoir les elements et les acteurs
        id_campagne = res['id_campagne']
        campagne = self.lire(id_campagne)
        return campagne
    
    def update(self, campagne : Campagne) -> None :
        """Met à jour la ligne correspondante à la campagne avec des nouvelles informations\n
        Attention : ne met pas à jour les cartes et les acteurs de la campagne (ni leur relation avec la campagne)

        Args:
            campagne (Campagne): campagne dont on veut mettre à jour les informations
        """
        id_campagne = campagne.id_campagne
        nom = campagne.nom_campagne
        nb_places_libres = campagne.nb_places_libres
        with DBConnection().connection as connection :
            with connection.cursor() as cursor :
                sql = """UPDATE campagne SET nom_campagne = '{}', nb_places_libres = {}
                WHERE id_campagne = {}""".format(nom, nb_places_libres, id_campagne)
                cursor.execute(sql)
            connection.commit()
    
    def delete(self, campagne: Campagne) -> None :
        """Supprime une ligne dans la table campagne\n
        Drop cascade permet de supprimer également les lignes lui correspondant dans les tables d'association

        Args:
            campagne (Campagne): objet de la camapgne que l'on veut supprimer de la base de données
        """
        id_campagne = campagne.id_campagne
        with DBConnection().connection as connection :
            with connection.cursor() as cursor :
                sql = """DELETE FROM campagne WHERE id_campagne={}""".format(id_campagne)
                cursor.execute(sql)
            connection.commit()
        # ne retourne rien

# -----------------------------------------------------------------------------------------------------

    def sauvegarder(self):
        # sauvegarder l'état actuel de la campagne (MJ)
        # récupération d'une ligne dans la table Campagne 
        # pas pour l'instant
        pass
    
    def importer(self):
        # pareil pas pour l'instant
        pass

    def changer_carte(self, campagne : Campagne, carte : Carte) -> Campagne:
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                id_campagne = campagne.id_campagne
                id_carte = carte.id_carte
                sql ="""UPDATE carte SET actuelle = FALSE WHERE id_campagne = {} AND actuelle = TRUE;
                        UPDATE carte SET actuelle = TRUE WHERE id_carte = {}""".format(id_campagne, id_carte)
                cursor.execute(sql)
            connection.commit()
        return campagne
        #L'objet ne change pas, mais par principe les updates renvoient un objet
        #Récupère la carte actuelle, change le bool, met a jour la ligne avec carte.id_carte comme id, renvoie une nouvelle campagne
        # changer la carte actuelle de la campagne (MJ)
        # modification de la table d'association ConstitutionCampagne
        # + création d'une nouvelle carte au besoin (use CarteDAO) (pas pour l'instant)

    def get_idcartes_de_campagne(self, campagne : Campagne) -> list:
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                id_campagne = campagne.id_campagne
                sql = """SELECT id_carte FROM carte WHERE id_campagne = {}""".format(id_campagne)
                cursor.execute(sql)
                res = cursor.fetchall()
                list_id_cartes = []
                for ligne in res:
                    id_carte = ligne["id_carte"]
                    list_id_cartes.append(id_carte)
        return list_id_cartes
    
    def get_idcampagnes_pas_pleines(self) -> list:
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                sql = """SELECT id_campagne FROM campagne WHERE nb_places_libres > 0"""
                cursor.execute(sql)
                res = cursor.fetchall()
                list_id_campagnes = []
                for ligne in res:
                    id_campagne = ligne["id_campagne"]
                    list_id_campagnes.append(id_campagne)
        return list_id_campagnes

    # def delete(self, campagne: Campagne):
    #     id_campagne = campagne.id_campagne
    #     with DBConnection().connection as connection:
    #         with connection.cursor() as cursor:
    #             sql = """DELETE FROM campagne WHERE id_campagne={}""".format(id_campagne)
    #             cursor.execute(sql)
    #         connection.commit()
