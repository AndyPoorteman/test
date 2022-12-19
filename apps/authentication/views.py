# -*- encoding: utf-8 -*-
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm


def login_view(request):#formulaire de connection
    form = LoginForm(request.POST or None)#enregistre dans une variable le formulaire de connection

    msg = None#initialise la variable message

    if request.method == "POST":#verifie que la methode est bien un reception d'information de l'utilisateur

        if form.is_valid():#is valid ?
            username = form.cleaned_data.get("username")#recuprere le nom d'utilisateur depuis formulaire   
            password = form.cleaned_data.get("password")#recuprere le mot de passe depuis le formulaire
            user = authenticate(username=username, password=password)#essai de connection utilisateur
            if user is not None: #verifie qu'il y a un client
                login(request, user)#connection
                return redirect("/")#redirection vers la page d'acceuil
            else:
                msg = 'Invalid credentials'#mauvais identifiant
        else:
            msg = 'Error validating the form'# erreur de validation

    return render(request, "accounts/login.html", {"form": form, "msg": msg})#genere la page de connection


""" def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = 'User created - please <a href="/login">login</a>.'
            success = True

            # return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success}) """
