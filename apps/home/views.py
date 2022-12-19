# -*- encoding: utf-8 -*-
#dependancy
from django.http import JsonResponse
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from .models import table_influx,imgSociete
from apps.scripts.data_influx import connect_influx,get_data
from json import dumps
import pandas as pd
import numpy as np
from django.core.serializers.json import DjangoJSONEncoder

@login_required(login_url="/login/")#assure la connection avant le chargement d'une page d'accueil
def index(request,url_parameter=1):
    
    userid = request.user.id#identifiant utilisateur
    influx = table_influx.objects.all()#formulaire admin(influx)
    img=imgSociete.objects.all()#logo de l'entreprise
    request.session['url_parameter']=url_parameter#n° page

    try: #assure que le code dessous retourne quelque chose de valable
        for flux in influx:#boucle les formulaire
         if userid == flux.client_id.id and url_parameter == flux.page:#recupère le formulaire correspondant au n° de page et a l'utilisateur connecté
           
                data,timestamp,titles,symbol,limit=connect_influx(listed = flux.series,database= flux.table)#retourne les differents éléments de la base de donnée influx
                if not titles:#s'assure que le titre est valable
                        titles=list(flux.series.keys())#recupere les titres de la base de donnée si titles vide
                break

        labels=dumps(timestamp,
                sort_keys=True,
                indent=1,
                cls=DjangoJSONEncoder
            )
        title=dumps(titles)
        datas=dumps(data)
        symbols=dumps(symbol)
        #transorme les listes d'influx au format json
        valid=True#enable download button
        context = {'data':datas,'label':labels,'title':title,'userid':userid,'img':img,'influx':influx,'symbols':symbols,'url_parameter':url_parameter,'limit':limit,'valid':valid}
        #permet de passer les differents éléments dans html
        if len(titles)==2:#analyse le nombre d'element
            html_template = loader.get_template('home/index_2.html')#charge la page pour deux graphiques
        else:
            if len(titles)==1:#analyse le nombre d'element
                html_template = loader.get_template('home/index_1.html')
            else:
                if len(titles)==3:#analyse le nombre d'element
                    html_template = loader.get_template('home/index_3.html')
                else:
                    if len(titles)==4:
                        html_template = loader.get_template('home/index_4.html')
                    else:
                        if len(titles)==5:
                            html_template = loader.get_template('home/index_5.html')
                        else:
                            if len(titles)==6:
                                html_template = loader.get_template('home/index_6.html')
                            else:
                                if len(titles)==7:
                                    html_template = loader.get_template('home/index_7.html')
                                else:
                                    if len(titles)==8:
                                        html_template = loader.get_template('home/index_8.html')
                
    except:#si le dessus n'est pas valide
        html_template = loader.get_template('home/page-412.html')#charge la page d'erreur 
        context={'userid':userid,'img':img,'influx':influx,'url_parameter':url_parameter}#permet de passer les differents éléments dans html
    
    return HttpResponse(html_template.render(context, request))#genere la page avec les parametres
    


def hello_world_view(request):
    userid = request.user.id
    influx = table_influx.objects.all()
    url_parameter=request.session['url_parameter']
    for flux in influx:
        if userid ==flux.client_id.id and url_parameter == flux.page:
            print('database',flux.table)
            data,time=get_data(flux.series,flux.table)
                #{"tur":["FNU",[0,500],'tur'],"ec":['PPM',[0,500],'ec'],"ph":['',[0,14],'pH'],"temp":['C°',[0,20],'temp']},database='Example')
    datas = dumps(data)
    labels = dumps(time)
    return JsonResponse({'datas':datas,'labels':labels},status=200)

