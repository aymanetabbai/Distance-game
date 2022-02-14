import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir)
sys.path.append(parentdir)

import unittest
from app.classes_web.personnage_web import PersonnageWeb
from app.classes_objet.personnage import Personnage

class TestPersonnageWeb(unittest.TestCase) :
    
    def test_get_bonus_abilities(self) :
        perso = Personnage(None, None, None, None, None, None, None, "dragonborn", "barbarian", None, None, None)
        test_perso_web = PersonnageWeb().get_bonus_abilities(perso)
        self.assertEqual(test_perso_web, {'STR': 2, 'CHA': 1})

    def test_get_strating_equipements(self) :
        perso = Personnage(None, None, None, None, None, None, None, "dragonborn", "barbarian", None, None, None)
        test_perso_web = PersonnageWeb().get_starting_equipements(perso)
        self.assertEqual(test_perso_web, {'explorers-pack': 1, 'javelin': 4})
        
    def test_get_hp_base(self) :
        perso = Personnage(None, None, None, None, None, None, None, "dragonborn", "barbarian", None, None, None)
        test_perso_web = PersonnageWeb().get_hp_base(perso)
        self.assertEqual(test_perso_web, 12)
        
if __name__ == '__main__' :
    unittest.main()
    web = TestPersonnageWeb()
    web.test_get_bonus_abilities()
    web.test_get_strating_equipements()
    web.test_get_hp_base()
    