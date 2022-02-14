import random
from typing import List
import PyInquirer

from PyInquirer import prompt, Separator
# from dotenv import load_dotenv

# load_dotenv()

# pas d'accents dans les commentaires mais ok dans les docs ?
questions = [
    {
        'type': 'input',
        'name': 'lancer_de',
        'message': 'Voulez-vous lancer un dé?'
    },
    {
        'type': 'input',
        'name': 'max_de',
        'message': 'valeur maximale du dé : '
    },
    {
        'type': 'input',
        'name': 'est_révélé',
        'message': 'faut-il le révéler ?'
    }
]

#answers = prompt(questions)
#print(answers)

questions = [
    {
        'type': 'input',
        'name': 'est_revele',
        'message': "Voules-vous que ce dé soit révélé à l'ensemble des joueurs ?"
        }
    ]

questions = [
    {
        'type': 'list',
        'name': 'max_de',
        'message': "A combien voulez-vous fixer le dé",
        'choices': [
            {
                'name' : 'Oui',
                'value' : 'True'
            },
            {
                'name' : 'Non',
                'value' : 'False'
            }]
        }
    ]

# answers2 = prompt(questions)
# deService = DeService()
# deLance = deService.lancerDe()
# joueurService = JoueurService()
# joueurService.mettreAJourDeJoueur(deLance)
# print(answers2)

questions = [
    {
        'type': 'expand',
        'message': 'Conflict on `file.js`: ',
        'name': 'overwrite',
        'default': 'a',
        'choices': [
            {
                'key': 'y',
                'name': 'Overwrite',
                'value': 'overwrite'
            },
            {
                'key': 'a',
                'name': 'Overwrite this one and all next',
                'value': 'overwrite_all'
            },
            {
                'key': 'd',
                'name': 'Show diff',
                'value': 'diff'
            },
            {
                'key': 'x',
                'name': 'Abort',
                'value': 'abort'
            }
        ]
    }
]

#answers3 = prompt(questions)
#print(answers3)

questions = [
    {
        'type': 'list',
        'name': 'est_revele',
        'message': "Voules-vous que ce dé soit révélé à l'ensemble des joueurs ?",
        'choices': [
            {
                'name' : 'Oui',
                'value' : 'True'
            },
            {
                'name' : 'Non',
                'value' : 'False'
            }]
        }
    ]

#answers = prompt(questions)
#print(answers)

questions = [
    {
        'type': 'input',
        'name': 'max_de',
        'message': "A combien voulez-vous fixer le dé ?"
        }
    ]

#answers = prompt(questions)
#print(answers)

import re

test = '1'

import regex

match = regex.match('[1-1]', test)
if match :
    print("OK")

#print(AccesUtilisateur().run())

# list = []
# for i in range(10) :
#     list.append((i, i*2))
# print(list)

# list_2 = []
# for item in list :
#     list_2.append(item[0])
# print(list_2)

# test = (2,1)
# print(isinstance(test, tuple), len(test), test[0])


# class Test :
#     def __init__(self, coordonnees : Coordonnees = None, nom = None) :
#         if not isinstance(coordonnees, Coordonnees) : 
#             print("c'est ok qd même")
#         self.coordonnees = coordonnees    
#         self.nom = nom
    
#     def __str__(self) :
#         self.nom
     
# coor = Coordonnees(1,1,1)
# test = Test()
# print(test.coordonnees, type(test.coordonnees))
# test2 = Test(1)
# print(test2.coordonnees, type(test2.coordonnees))
# test3 = Test(coor, "test")
# print(test3.coordonnees, type(test3.coordonnees))

# s = "nom : {}".format(test3.nom)
# print(s)

# verifier format nom des tables (cf public."De")

# AccesUtilisateur().run()
# EntreeCampagne().run()

        
# position = Coordonnees(1, 1, 1)
# carte = Carte(1, None, None, position, None)
# element = Equipement(None, carte, position, None, None)
# CarteService.verif_element_position(carte, element)

# agnou = Utilisateur('agnou', 'mdp', None)
# acteurs = UtilisateurService.get_idacteurs_utilisateur(agnou)
# print(acteurs)

questions = [
    {
        'type': 'checkbox',
        'qmark': '🐹',
        'message': 'Select your Pokemon Team',
        'name': 'pokemons',
        'choices': [ 
            Separator('🔥Fire Starter')
            ,{'name':'Charmander'}
            ,{'name':'Cyndaquil'}
            ,{'name':'Torchic'}
            ,{'name':'Chimchar'}
            ,{'name':'Oshawott'}
            ,Separator('🚿Water starter')
            ,{'name':'Squirtle'}
            ,{'name':'Totodile'}
            ,{'name':'Mudkip'}
            ,{'name':'Turtwig'}
            ,{'name':'Tepig'}
            ,Separator('🌱Grass starter')
            ,{'name':'Bulbasaur'}
            ,{'name':'Chikorita'}
            ,{'name':'Treecko'}
            ,{'name':'Piplup'}
            ,{'name':'Snivy'}
        ],
    }
]

# from app.classes_ihm.authentification.menu_authentification import MenuAuthentification

# current_view = MenuAuthentification()
# with open('Classes_IHM/graphical_assets/banner.txt', 'r', encoding="utf-8") as asset:
#     print(asset.read())
# while current_view : 
#     with open('Classes_IHM/graphical_assets/border.txt', 'r', encoding="utf-8") as asset:
#         print(asset.read())
#     current_view.display_info()
#     current_view = current_view.make_choice()

# liste = [i for i in range(10)]
# print(liste[0:9])

# try :
#     joueur = ActeurService.creer('agnou', False)
#     perso = PersonnageService().creer(joueur, coordonnees, 'personnage', "dragonborn", "barbarian", 10, 15, 5)
#     print(perso.equipements)
# except KeyError :
#     print('NOT OK')

# from Classes_web.personnage_web import PersonnageWeb

# print(PersonnageService.get_all_races_and_classes())

# from app.classes_web.equipement_web import EquipementWeb

# javelin = Equipement(1, coordonnees, 'javelin', True)
# print(EquipementWeb().get_damage_dice(javelin))
# print(EquipementWeb().get_range(javelin))

# changer nom des dossiers? (minuscules)
# changer requirements (pas besoin fastapi et uvicorn ?)
# README
# generer les docs 
# creer un monstre hors de l'api
# dossier app

damage_dice = '2d6'
damage_dice = [int(i) for i in damage_dice.split('d')]
for i in range(damage_dice[0]) :
    print(i)

print(random.randrange(1, 4+1))

txt = "Adult black dragon"
index = "adult-black-dragon"
x = index.lower().replace(' ', '-')
print(x)

import os 

salt = os.urandom(32)
test = hash('password')
print(test.__class__)

from app.classes_objet.de import De
from app.classes_dao.de_dao import DeDAO

de = De(None, 1, 1, False, False)

with open('app/Classes_IHM/graphical_assets/banner.txt', 'r', encoding="utf-8") as asset:
    print(asset.read())
    
print(de.__class__)

from app.classes_service.coordonnees_service import CoordonneesService
from app.classes_service.element_service import ElementService

# coordonnees1 = CoordonneesService.creer(1, 1)
# coordonnees2 = CoordonneesService.creer(1, 2)
# club = ElementService.creer(coordonnees1, "club", True, False)
# print(club.__class__)
# dragon = ElementService.creer(coordonnees2, "adult-silver-dragon", True, True)
# print(dragon.hp)
# print(ElementService.damage_dice_int(club))
from app.classes_dao.coordonnees_dao import CoordonneesDAO
from app.classes_dao.element_dao import ElementDAO
from app.classes_objet.coordonnees import Coordonnees
coord = Coordonnees(1, 1, 1)
# element = ElementDAO().lire(2)
# element.position = CoordonneesDAO().lire(element.position)
# print(isinstance(element.est_revele, bool))
print(coord)
