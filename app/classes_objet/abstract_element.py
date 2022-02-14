from abc import ABC
import regex
from app.classes_objet.coordonnees import Coordonnees
from unittest import TestCase

# La doc est a refaire !!!

class AbstractElement (ABC): 
    '''
    Une classe abstraite représentant un élément sur une carte. Un élément peut être un monstre ou un équipement par exemple.
    '''

    def __init__(self, id_element : int, coordonnees : Coordonnees, id_api : str, est_revele : bool) :   
        '''
        Constructeur de la classe AbstractElement

        Attributes
        ----------------------------------------------------------------------------------------------------

        id_element : int : entier représentant l'id de l'élément dans la base de données.
        coordonnees : Coordonnees : coordonnées de l'élément. Doit être sous la forme d'une instance de la classe Coordonnees
        id_api : str : chaîne de caractères représentant l'id de l'élément dans l'API.
        est_revele : bool : booléen qui prend la valeur True si l'élément est révélé sur la carte et False sinon.

        Examples
        ----------------------------------------------------------------------------------------------------

        coordonnees_arrow = Coordonnees("id_coor_arrow", 1, 1)
        coordonnees_black_bear = Coordonnees("id_coor_black_bear", 10, 25)
        arrow = AbstractElement(0001, coordonnees_arrow, "arrow", True)      
        black_bear = AbstractElement(0002, coordonnees_black_bear, "black-bear", False)        
        '''        
        self.id_element = id_element
        self.position = coordonnees
        self.id_api = id_api
        self.est_revele = est_revele 
        
    def reveler(self) :
        '''
        Cette méthode permet au MJ révéler au joueur un élément qui n'a pas encore été révélé.
        Si l'élément en question a déjà était révélé, la méthode renvoit un message d'erreur.
        
        Parameters : 
        ----------------------------------------------------------------------------------------------------
        
        Examples :
        ----------------------------------------------------------------------------------------------------

        # Cas où l'élément est déjà révélé.

        arrow_revele = arrow.est_revele
        print(arrow_revele)
        arrow.reveler()

        # Cas où l'élément n'est pas encore révélé.

        black_bear_revele = black_bear.est_revele
        print(black_bear_revele)
        black_bear.reveler()
        new_black_bear_revele = black_bear.est_revele
        print(new_black_bear_revele)
        '''
        if self.est_revele :
            raise Exception("L'élément est déjà révélé.")
        else :
            self.est_revele = True
    
    def check_incarte_position (self, x, y) :
        '''
        Cette méthode de classe vérifie si les coordonnées de l'élément sont inclus dans les coordonnées de la carte.
        On vérifie que l'élément n'est pas en-dehors de la carte. S'il est en-dehors, la méthode renvoit une erreur.

        Parameters :
        ----------------------------------------------------------------------------------------------------

        x : int : La valeur de la coordonnée en abscisse de l'élément à vérifier.
        y : int : La valeur de la coordonnée en ordonnée de l'élément à vérifier.

        Examples : 
        ----------------------------------------------------------------------------------------------------

        # Cas où l'élément est bien dans la carte.

        x = arrow.coordonnees[0]
        y = arrow.coordonnees[1]
        check_incarte_position(x, y)

        # Cas où l'élément est en-dehors de la carte.

        x = black_bear.coordonnees[0]
        y = black_bear.coordonnees[1]
        check_incarte_position(x, y)
        '''
        pattern_x = '[1-' + str(self.carte.taille_x) + ']'
        pattern_y = '[1-' + str(self.carte.taille_y) + ']'
        if not regex.match(pattern_x, str(x)) or not regex.match(pattern_y, str(y)):
            raise ValueError
    
    def set_coordonnees(self, coordonnees : Coordonnees) :
        '''
        Cette méthode de classe permet de modifier les coordonnées d'un élément. Cela permet de modéliser le déplacement d'un monstre sur la carte par exemple.
        Cette méthode vérifie également si les coordonnées sont valides aux vues de la taille de la carte grâce à la méthode "check_incarte_position".

        Parameters :
        ----------------------------------------------------------------------------------------------------

        coordonnees : Coordonnees : Les nouvelles coordonnées de l'élément. Accepte uniquement une instance de la classe Coordonnees.

        Example :
        ----------------------------------------------------------------------------------------------------

        new_coordonnees = Coordonnees(id_coordonnees, 2, 2)

        print(arrow.coordonnees)
        arrow.set_coordonnees(new_coordonnees_arrow)
        print(arrow.coordonnees)
        '''
        self.position = coordonnees
        self.check_incarte_position(coordonnees.coordonnee_x, coordonnees.coordonnee_y)
        self.position_x = coordonnees.coordonnee_x
        self.position_y = coordonnees.coordonnee_y


class TestAbstractElement(TestCase) : 

    def is_reveler_ok(self) :      
        
        coordonnees_black_bear = Coordonnees("id_coor_black_bear", 10, 25)             
        black_bear = AbstractElement(2, coordonnees_black_bear, "black-bear", False)
        black_bear.reveler()
        self.assertTrue(black_bear.est_revele)

    def is_check_incarte_position_ok(self) : 

        coordonnees_arrow = Coordonnees("id_coor_arrow", 1, 1)        
        arrow = AbstractElement(1, coordonnees_arrow, "arrow", True)      
        # La méthode check_incarte_position renvoit quel type d'objet ? Renvoit-elle quelque chose ? Un booléen ?
        
    
    def is_set_coordonnees_ok(self) :
        coordonnees_arrow = Coordonnees("id_coor_arrow", 1, 1)
        arrow = AbstractElement(1, coordonnees_arrow, "arrow", True)        
        new_coordonnees_arrow = Coordonnees('id_new_coor_arrow', 2, 2)        
        arrow.set_coordonnees(new_coordonnees_arrow)
        self.assertIs(arrow.coordonnees, new_coordonnees_arrow)
        
    def set_coordonnees_shouldBeFalse(self) :         
        coordonnees_arrow = Coordonnees("id_coor_arrow", 1, 1)
        new_coordonnees_arrow = Coordonnees('id_new_coor_arrow', 2, 2)        
        arrow = AbstractElement(1, coordonnees_arrow, "arrow", True)       
        arrow.set_coordonnees(new_coordonnees_arrow)
        self.assertIsNot(arrow.coordonnees, coordonnees_arrow)


