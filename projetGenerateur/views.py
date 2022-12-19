from django.shortcuts import render 

#afficher la page d'accueil
def afficherAccueil(request):
    return render(request, 'accueil.html')

#accéder au générateur depuis l'accueil
def accessGenerator(request):
    #pour construire la liste déroulante
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
    return render(request, 'generateur.html', {'language_list': language_list,
                                                'cat_list': cat_list})