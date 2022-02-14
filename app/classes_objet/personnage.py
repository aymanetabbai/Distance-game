from typing import List
from app.classes_objet.coordonnees import Coordonnees
from app.classes_objet.joueur import Joueur
from app.classes_objet.equipement import Equipement

class Personnage :

    def __init__(self, id_personnage : int, joueur : Joueur, position : Coordonnees, nom_personnage : str, id_api_race : str, id_api_classe : str, hp : int, attaque : int, defense : int, vitesse : int, niveau : int =1, equipements : List[Equipement] = []) -> None :
        self.id_personnage = id_personnage 
        self.position = position
        self.joueur = joueur
        self.nom_personnage = nom_personnage
        self.id_api_race = id_api_race
        self.id_api_classe = id_api_classe
        self.hp = hp
        self.attaque = attaque
        self.defense = defense
        self.vitesse = vitesse
        self.niveau = niveau
        self.equipements = equipements
        
    def __str__(self) : 
        str_personnage = "Personnage {}, id {}, joueur : {}, race : {}, classe : {}".format(self.nom_personnage, self.id_personnage, self.joueur.nom_utilisateur, self.id_api_race, self.id_api_classe)
        return str_personnage
    
    def add_equipement(self, equipement : Equipement) -> None :
        # contrainte pour que forcement la position soit la meme ?
        # supprimer de la carte
        equipement.position = self.position
        equipement.est_revele = True
        self.equipements.append(equipement)
        
    def consulter_caracteristiques(self) -> str :
        str_caracteristiques = 'attaque : {}, défense : {}, vitesse : {}, hp : {}, niveau : {}.'.format(self.attaque, self.defense, self.vitesse, self.hp, self.niveau)
        return str_caracteristiques

    