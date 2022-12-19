from .models import *
import random
import re
from nltk.lm.preprocessing import pad_both_ends
import mchmm as mc
import pandas as pd
import random

#dans ce fichier, on met les fonctions qui nous servent pour faire tourner notre code

#fonction pour transformer les données number du form en integer
def parseInt(s):
    try:
        return int(s)
    except ValueError:
        return 0

#le code du générateur qu'on appele ensuite dans le fichier views.py

def genSeq(maxSize, letterStart, matrix, previousStart=None):
    """Cette fonction est une fonction récursive qui permet de générer tous les mots possibles à partir des
    chaines de Markov calculées avec la class DataFrame. Elle prend en entrée la taille max des mots, une instance
    de la classe DataFrame et retourne une liste de toutes les séquences possibles."""
    #si c'est la première itération de la fonction, on initialise la valeur de previousStart
    if not previousStart:
        previousStart=letterStart
    #on récupère les données
    mostFreq = matrix.loc[letterStart].sort_values(ascending=False)
    freqSup0 = mostFreq[mostFreq>0]
    #variable pour stocker les séquences
    listeSeq = []
    #stocker toutes les combinaisons de séquences possibles
    for newStart in freqSup0.index:
        seq = f'{previousStart}.{newStart}'
        if not len(seq.split('.')) == maxSize+1:#+1 à cause de la balise de début de mot
            #on change les arguments de la fonction
            seq = genSeq(maxSize, newStart, matrix, previousStart=seq)
        listeSeq.append(seq)
    return listeSeq

def flattenList(liste):
    """Cette fonction est récursive et permet de d'applatir une liste irrégulière.
    Elle retourne un générateur."""
    for element in liste:
        if isinstance(element, list):
            yield from flattenList(element)
        else:
            yield element

class Generateur:
    """Cette classe permet de générer des mots selon les choix de l'utilisateur. Elle
    prend en entrée la langue, la catégorie, le nombre de mots et la taille maximum
    des mots. Ces données sont choisies par l'utilisateur."""
    def __init__(self, langue, categorie, nbWord, sizeWord):
        self.langue = langue
        self.categorie = categorie
        self.nbWord = nbWord
        self.sizeWord = sizeWord

    def selectFile(self):
        """Cette fonction permet d'ouvrir le fichier de mots correspondant aux choix de l'utilisateur.
        On retourne une liste qui contient le nombre de mots choisis par l'utilisateur."""
        #ouvrir le fichier correspondant aux choix de l'utilisateur
        #chercher le fichier correspondant à la langue et la catégorie choisie
        if self.langue == "en" and self.categorie == "noun":
            data = EnNoun.objects.all()
        #on transforme les données en list
        strData = str(data)
        listData = strData.split('\n')
        #on nettoie la liste
        liste = [re.sub('\r', '', sub) for sub in listData]
        del liste[0]
        #choisir aléatoirement le nombre de mots choisis par l'utilisateur dans toutes
        #la liste de mots réels
        #le code ne fonctionne pas si on choisit de générer moins de 20 mots
        #car il n'y a pas assez de données de départ
        #pour que l'utilisateur puisse générer moins de 20 mots s'il le souhaite, 
        #on rajoute la valeur de 20 au nombre de mots choisis par l'utilisateur
        #et on génére les mots à partir du nombre de mots choisis + 20
        #on retournera à la fin du programme le nombre de mots choisi par l'utilisateur
        if self.nbWord >= 20:
            count = self.nbWord
        else:
            count = self.nbWord + 20
        result = random.sample(liste, count)
        return result

    def sepGrams(self):
        """Cette fonction permet de séparer les mots (on sépare là où il y a des points).
        On ajoute des balises qui marque le début et la fin des mots."""
        #on instancie la liste de mots utilisés par cette fonction
        liste = self.selectFile()
        #on sépare les mots là où il y a des points
        liste = [element.split('.') for element in liste]
        #on ajoute les balises de fin de mot (</s>) et début de mot (<s>)
        cutCorpus = []
        for sousListe in liste:
            element = list(pad_both_ends(sousListe, n=2))
            cutCorpus.append(element)
        return cutCorpus

    def createMatrix(self):
        """Cette fonction permet d'obtenir une matrice qui contient les fréquences de lettres
        possibles calculées avec les chaines de Markov."""
        liste = self.sepGrams()
        #utiliser la librairie python mchmm pour calculer les chaines de Markov
        markov = mc.MarkovChain().from_data([x for y in liste for x in y])
        df = pd.DataFrame(markov.observed_matrix, index=markov.states, columns=markov.states, dtype=int)
        return df

    def lastLetter(self):
        """Cette fonction permet d'obtenir les lettres qui peuvent apparaître en fin de mot."""
        matrix = self.createMatrix()
        #on ne garde que les lettres suivies de </s> et dont la fréquence est supérieure à 0
        lastDF = pd.DataFrame(matrix['</s>'][matrix['</s>']>0])
        #le transformer en liste
        listLastLetter = lastDF.index.values.tolist()
        return listLastLetter

    def generer(self):
        """Cette fonction permet de générer des mots inventés, et de nettoyer la liste de 
        résultats obtenues."""
        #on instancie les fonctions précédentes
        #les mots déjà existants
        originalWords = self.selectFile()
        #la matrice des séquences de lettres
        matrix = self.createMatrix()
        #la matrice des dernières lettres possibles
        lastSeq = self.lastLetter()
        #on supprime les balises de fin de mots de la matrice pour ne pas qu'elle 
        # n'apparaisse pas en milieu de mot
        del matrix['</s>']
        #on appelle la fonction pour générer les mots
        genWords = genSeq(self.sizeWord, '<s>', matrix, previousStart=None)
        #on applatit la liste irrégulière et on la transforme en liste
        genWords = list(flattenList(genWords))
        #on supprime les balises de fin de mots et début de mot
        #on vérifie que les mots ne sont pas des mots existant dans la base de données
        cleanWords = []
        for element in genWords:
            element = element.replace('<s>.', '')
            element = element.replace('</s>', '')
            if element not in originalWords:
                cleanWords.append(element)
        #on sépare les éléments de la liste à chaque point
        #c'est pour vérifier que le dernier groupe de lettres de la séquence
        #peut bien être en fin de mot
        result = []
        for element in cleanWords:
            word = element.split('.')
            if word[self.sizeWord-1] in lastSeq:
                result.append(word)
        #on ne garde que le nombre de mots choisis par l'utilisateur
        genWords = random.sample(result, self.nbWord)
        #on joint les groupes de lettres des éléments ensemble
        mots = [''.join(element) for element in genWords]
        #vérifier qu'il y a bien au moins une voyelle dans les mots
        vowels = ['a', 'e', 'i', 'o', 'u', 'y']
        motInvente = []
        for words in mots:
            for letters in words:
                if letters in vowels and words not in motInvente:
                    motInvente.append(words)
        #on retourne la liste de mots inventés
        return motInvente