#from turtle import bgcolor, right
from influxdb import DataFrameClient,InfluxDBClient
import numpy as np
import os
import pandas as pd
from django.shortcuts import render
import mimetypes

def connect_influx(listed = {"tur":["FNU",[0,500]],"ec":['PPM',[0,500]],"ph":['pH',[0,14]],"temp":['Celsius',[0,20]]},database="example"): 
    #listed contient le symbole des donnée de la sonde ainsi que le min/max
    #datab ase contient la base de donnée influx
    titles=list(listed.keys())
    
    client = DataFrameClient(host='connect-bsens.ddns.net',
                                port=8086,
                                ssl=True,verify_ssl=True,database=database)
    """   """
    #creation du dashboard
    if len(titles)>1:
        
                 #lumn=1
        for target in titles:
            
            #on querry dans la base de donnée
            res = client.query("select * from {} where time > 20-03-2022".format(listed[target][2]))
            #on arrondit à deux  decimal
            data=np.around(res[listed[target][2]].values,decimals=2)
            #on passe le format de donnée de [[x1],[x2],[x3]] à [x2,x2,x3]
            final=list(np.concatenate(data).flat)
            #on change le fuseau horaire et change la colonne du temps
            df=pd.DataFrame(final,columns=[listed[target][2]],index=res[listed[target][2]].index.tz_convert('Europe/Brussels'))
            df.reset_index(inplace=True)
            df = df.rename(columns={'index':'timestamp'})
            #ajoute le graf associé à une donnée
           
            
    else:
        for target in titles:
            
            res = client.query("select * from {} where time > 20-03-2022".format(listed[target][2]))
                #on arrondit à deux  decimal
            data=np.around(res[listed[target][2]].values,decimals=2)
                #on passe le format de donnée de [[x1],[x2],[x3]] à [x2,x2,x3]
            final=list(np.concatenate(data).flat)
                #on change le fuseau horaire et change la colonne du temps
            df=pd.DataFrame(final,columns=[listed[target][2]],index=res[listed[target][2]].index.tz_convert('Europe/Berlin'))
            df.reset_index(inplace=True)
            df = df.rename(columns={'index':'timestamp'})
            df = df.rename(columns={listed[target][2]:listed[target][0]})
            
            

    return df



def influx2(listed = {"tur":["FNU",[0,500]],"ec":['PPM',[0,500]],"ph":['pH',[0,14]],"temp":['Celsius',[0,20]]},database="Limpido2"):
    titles=list(listed.keys())
    client = DataFrameClient(host='connect-bsens.ddns.net',
                                port=8086,
                                ssl=True,verify_ssl=True,database=database)
    
    #creation du dashboard
    fig = make_subplots(rows=2, cols=2,
        shared_xaxes='all',
        horizontal_spacing=0.065,
        vertical_spacing=0.15,
        subplot_titles=titles,
        )

    row=1
    lumn=1
    for target in titles:
        #on querry dans la base de donnée
        res = client.query("select * from {} where time >now()-60d".format(listed[target][2]))
        #on arrondit à deux  decimal
        data=np.around(res[listed[target][2]].values,decimals=2)
        #on passe le format de donnée de [[x1],[x2],[x3]] à [x2,x2,x3]
        final=list(np.concatenate(data).flat)
        #on change le fuseau horaire et change la colonne du temps
        df=pd.DataFrame(final,columns=[listed[target][2]],index=res[listed[target][2]].index.tz_convert('Europe/Berlin'))
        df.reset_index(inplace=True)
        df = df.rename(columns={'index':'timestamp'})
        #ajoute le graf associé à une donnée
        fig.add_trace(  
            go.Scatter(x=df.timestamp,y=final,
                    name=listed[target][0],line=dict(color='Blue', width=3)),
        row=row, col=lumn
        )
        #ajustement de l'affichage
        fig.update_layout(autosize=True,
                    height=850,
                    xaxis2_rangeselector_visible=False,
                    xaxis3_rangeselector_visible=False,
                    xaxis4_rangeselector_visible=False,
                    xaxis_type="date"
                    ,paper_bgcolor="rgba(0,0,00,0)",
                    modebar={"bgcolor":"hsl(0,0,100)","color":"black"},
                     yaxis = dict( tickfont = dict(size=14)),
                     xaxis = dict( tickfont = dict(size=14)),
                     title_font_size=20)
        fig.update_annotations(font_size=20)
        #barre de plages horaire
        fig.update_xaxes( 
                rangeselector=dict(
                    buttons=list([
                        dict(count=12, label="12h", step="hour", stepmode="todate"),
                        dict(count=1, label="1d", step="day", stepmode="backward"),
                        dict(count=7, label="7d", step="day", stepmode="backward"),
                        dict(count=1, label="1m", step="month", stepmode="backward"),
                        dict(step="all")
                    ])
                ),rangeselector_y=1.04,side="top" 
            )
            #ajustement du min/max des données
        fig.update_yaxes(range=listed[target][1],
        row=row, col=lumn,
        )
    

        if(lumn >= 2):
            row+=1
            lumn=1
        else:
            lumn+=1

    return fig,df