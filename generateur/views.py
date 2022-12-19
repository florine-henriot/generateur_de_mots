from django.shortcuts import render
from .fonctions import *
from .models import *

# Create your views here.

def afficherMot(request):
    #construire la liste déroulante
    language_list = [
        {'key': '', 'label': 'Langue'},
        {'key': 'en', 'label': 'Anglais'},
        {'key': 'fr', 'label': 'Français'},
    ]
    cat_list = [
        {'key': '', 'label': 'Catégorie'},
        {'key': 'noun', 'label': 'Noms'},
        {'key': 'verb', 'label': 'Verbes'},
        {'key': 'adj', 'label': 'Adjectifs'}
    ]
    #on récupère les données du formulaire entrées par l'utilisateur
    langue = request.POST.get('langue')
    categorie = request.POST.get('cat')
    nbMot = parseInt(request.POST.get('nbMot'))
    sizeMot = parseInt(request.POST.get('sizeMot'))
    #en premier on s'assure que l'utilisateur à correctement rempli le formulaire
    #liste message qui va contenir les messages d'erreurs s'il y en a
    message = []
    unavailableLang = ['fr']
    unavailableCat = ['verb', 'adj']
    if langue == '':
        message.append("Il faut choisir une langue.")
    if langue in unavailableLang:
        message.append("Le générateur ne fonctionne pas encore pour le français.")
    if categorie == '':
        message.append("Il faut choisir une catégorie.")
    if categorie in unavailableCat:
        message.append("Le générateur ne fonctionne pas encore pour les verbes et les adjectifs.")
    if nbMot <= 0:
        message.append("Il faut générer au moins 1 mot !")
    #le programme du générateur ne permet pas de générer assez de mots de moins de trois lettres
    if sizeMot <=2:
        message.append("La taille des mots doit être supérieure à 2.")
    #si la liste message n'est pas vide, on envoie les messages d'erreur à l'utilisateur
    if len(message) > 0:
        return render(request, 'generateur.html', {'message': message, 
                                                    'language_list': language_list, 
                                                    'cat_list': cat_list})
    #sinon, on envoie les résultats à l'utilisateur
    else:
        generateur = Generateur(langue, categorie, nbMot, sizeMot)
        result = generateur.generer()

        return render(request, 'generateur.html', {'resultat': result, 
                                                'language_list': language_list, 
                                                'cat_list': cat_list})