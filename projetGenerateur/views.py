from django.shortcuts import render 

def afficherAccueil(request):
    return render(request, 'accueil.html')

def accessGenerator(request):
    return render(request, 'generateur.html')