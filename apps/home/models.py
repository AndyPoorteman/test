# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.
def jsonCall():
        return {"data": ["symbol", ["Ymin", "Ymax"], "serie", "Title"]}

class table_influx(models.Model):#tableau des formulaires influx
    id = models.AutoField(primary_key=True,unique=True)#identifiant form
    client_id = models.ForeignKey(settings.AUTH_USER_MODEL,null = False,on_delete=models.CASCADE)#identifiant utilisateur
    series = models.JSONField(default=jsonCall)#parametre base de données influx
    page= models.IntegerField()#n°de page
    table = models.CharField(max_length=50, null = True)#nom base de données influx    
    site=models.CharField(max_length=50, null = True)  #titre
    
    def __str__(self):
        return (str)((str)(self.client_id )+(str)(self.site))#nom dans django admin

class imgSociete(models.Model):#tableau  de logo des société
    id = models.AutoField(primary_key=True,unique=True)#identifiant form
    client_id = models.ForeignKey(settings.AUTH_USER_MODEL,null = False,on_delete=models.CASCADE)#identifiant utilisateur
    logo=models.ImageField(upload_to="images")#image
    def __str__(self):
        return (str)(self.client_id)#nom dans django admin
    class Meta:
        db_table ="gallery"
