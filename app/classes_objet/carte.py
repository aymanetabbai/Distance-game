from typing import List
from app.classes_objet.abstract_element import AbstractElement
from app.classes_objet.coordonnees import Coordonnees

class Carte :

    def __init__(self, id_carte : int, nom_carte : str, coordonnees : Coordonnees, est_actuelle : bool, elements : List[AbstractElement] = []) -> None :
        self.id_carte = id_carte
        self.nom_carte = nom_carte
        self.elements = elements
        self.taille = coordonnees
        self.est_actuelle = est_actuelle
        
    def __str__(self) -> str :
        str_carte = 'Carte {}, id {}, taille : {}, {}'.format(self.nom_carte, self.id_carte, self.taille.coordonnee_x, self.taille.coordonnee_y)
        if self.est_actuelle :
            str_carte += ', carte actuelle'
        return str_carte
        
    def check_incarte_position(self, element_test : AbstractElement) -> None :
        # verifie que les deux coordonnees de element_test
        # sont bien comprises entre 1 et la taille de la carte
        # horizontalement (x) et verticalement (y)
        print(element_test)
        x = element_test.position.coordonnee_x
        y = element_test.position.coordonnee_y
        if not 1<=x<=self.taille.coordonnee_x or not 1<=y<=self.taille.coordonnee_y :
            raise ValueError
        
    def check_no_element_position(self, element_test : AbstractElement) -> None : 
        # verifie qu'aucun element ne se trouve deja a la meme position que element_test
            for element in self.elements : 
                # necessaire pour modifier la position d'un element de la carte
                if element.id_element != element_test.id_element :
                    if element.position.coordonnee_x == element_test.position.coordonnee_x and element.position.coordonnee_y == element_test.position.coordonnee_y :
                        raise ValueError
        
    def verif_element_position(self, element_test : AbstractElement) -> None :
        # execute les deux verifications ci-dessus
        self.check_incarte_position(element_test)
        self.check_no_element_position(element_test)

    def add_element(self, element : AbstractElement) -> None :
        # on verifie que les coordonnees de l'element satisfont les conditions de la carte
        self.verif_element_position(element)
        # on ajoute l'element a la liste des elements de la carte
        self.elements.append(element)