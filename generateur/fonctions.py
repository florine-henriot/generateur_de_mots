from .models import *
import random
import re

#dans ce fichier, on met les fonctions qui nous servent pour faire tourner notre code

#fonction pour transformer les données number en integer
def parseInt(s):
    try:
        return int(s)
    except ValueError:
        return 0

#le code du générateur qu'on appele ensuite dans le fichier views.py
class Generateur:
    def __init__(self, langue, categorie, nbMot):
        self.langue = langue
        self.categorie = categorie
        self.nbMot = nbMot

    def cleanData(self):
        """Fonction pour préparer la liste de mots à utiliser."""
        #chercher le fichier correspondant à la langue et la catégorie choisie
        if self.langue == "en" and self.categorie == "noun":
            data = EnNoun.objects.all()
        #on transforme les données en lits
        strData = str(data)
        listData = strData.split('\n')
        #on nettoie la liste
        noLineBreak = [re.sub('\r', '', sub) for sub in listData]
        del noLineBreak[0]
        return noLineBreak

    def selectNumber(self):
        """Fonction pour stocker aléatoirement le nombre de mots demandé par l'utilisateur."""
        #appel de la fonction précédente
        liste = self.cleanData()
        result = random.sample(liste, self.nbMot)
        return result