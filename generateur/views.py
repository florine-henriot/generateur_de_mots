from django.shortcuts import render
from .fonctions import *
from .models import *

# Create your views here.

def afficherMot(request):
    #on récupère les données du formulaire entrées par l'utilisateur
    langue = request.POST.get('langue')
    categorie = request.POST.get('cat')
    nbMot = parseInt(request.POST.get('nbMot'))

    #en premier on s'assure que l'utilisateur à correctement rempli le formulaire
    #liste message qui va contenir les messages d'erreurs s'il y en a
    message = []
    if langue == None:
        message.append("Il faut choisir une langue.")
    if categorie == None:
        message.append("Il faut choisir une catégorie.")
    if nbMot <= 0:
        message.append("Il faut choisir au moins 1 mot !")

    #si la liste message n'est pas vide, on envoie les messages d'erreur à l'utilisateur
    if len(message) > 0:
        return render(request, 'generateur.html', {'message': message})
    #sinon, on envoie l'utilisateur sur la page de résultat
    else:
        generateur = Generateur(langue, categorie, nbMot)
        result = generateur.selectNumber()

        return render(request, 'resultat.html', {'resultat': result})