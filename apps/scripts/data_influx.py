from influxdb import DataFrameClient
import numpy as np
import os
import pandas as pd
from django.shortcuts import render
import mimetypes
with open('/home/Bsens/ssl/pass.txt') as p:
    DB_PASSWORD = p.read().strip()
def connect_influx(listed = {"tur":["FNU",[0,10],'tur','Turbidity'],"ec":['PPM',[0,500],'ec','Conductivity'],"ph":['',[0,14],'pH',''],"temp":['C°',[0,20],'temp','Temperature']},database="Limpido2"): 
    #listed contient le symbole des donnée de la sonde ainsi que le min/max
    #database contient la base de donnée influx 
    keywords=list(listed.keys())
    
    client = DataFrameClient(host='connect-bsens.ddns.net',
                                username='Bsens',password=DB_PASSWORD,
                                port=8086,
                                ssl=True,verify_ssl=True,database=database)#permet de se connecter au serveur influx
    #init des listes des variables
    dataframe=[]
    timeframe=[]
    titles=[]
    symbols=[]
    limit=[]
    #creation du dashboard
    if len(keywords)>1:#verifie qu'il y a plus qu'un type de donnée à affiché 
        for target in keywords:
            limit.append(listed[target][1])#limite haute et basse du graphique
            
            res = client.query("select * from {} ".format(target))#on querry dans la base de donnée
            
            data=np.around(res[target].values,decimals=2)#on arrondit à deux  decimal
            #on change le fuseau horaire et change la colonne du temps
            index= res[target].index.tz_convert('Europe/Brussels')#changement du fuseau horaire
            index=index.strftime("%Y-%m-%d %H:%M:%S")# formatage heure date
            final=list(np.concatenate(data).flat)#on passe le format de donnée de [[x1],[x2],[x3]] à [x2,x2,x3] (liste de 1 dimension)
            #on ajoute les diferents elements au liste initié plus haut
            timeframe.append(index.tolist())#donnée x
            dataframe.append(final)   #donnée y
            symbols.append(listed[target][0])#symbol axe y
            titles.append(listed[target][3])#titres des graph

            
    else:#sinon
        for target in keywords:
            limit.append(listed[target][1])#limite haute et basse du graphique
            res = client.query("select * from {} where time > 20-03-2022".format(listed[target][2]))
                #on arrondit à deux  decimal
            data=np.around(res[target].values,decimals=2)
                #on passe le format de donnée de [[x1],[x2],[x3]] à [x2,x2,x3]
            final=list(np.concatenate(data).flat)
                #on change le fuseau horaire et change la colonne du temps
            index= res[target].index.tz_convert('Europe/Brussels')
            index=index.strftime("%Y-%m-%d %H:%M:%S")
            dataframe.append(final)
            timeframe.append(index.tolist())
            symbols.append(listed[target][0])
            titles=titles.append(listed[target][3])
    return dataframe,timeframe,titles,symbols,limit


def get_data(listed,database):
    titles=list(listed.keys())
    client = DataFrameClient(host='connect-bsens.ddns.net',
                                port=8086, username='Bsens',password=DB_PASSWORD,
                                ssl=True,verify_ssl=True,database=database)
    dataframes=[]
    timeframes=[]
    for target in titles:
        #on querry dans la base de donnée
        res = client.query("select * from {} where time >now()-60d".format(listed[target][2]))
        #on arrondit à deux  decimal
        data=np.around(res[listed[target][2]].values,decimals=2)
        #on passe le format de donnée de [[x1],[x2],[x3]] à [x2,x2,x3]
        final=list(np.concatenate(data).flat)
        #on change le fuseau horaire et change la colonne du temps
        index= res[target].index.tz_convert('Europe/Brussels')
        index=index.strftime("%Y-%m-%d %H:%M:%S")
        #df=pd.DataFrame(final,columns=[listed[target][2]],index=res[listed[target][2]].index.tz_convert('Europe/Brussels'))
        timeframes.append(index[-1])
        dataframes.append(final[-1]) 
    return dataframes,timeframes