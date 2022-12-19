import os
import sys
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE','core.settings')
django.setup()
from django.contrib.auth.models import User
from apps.home.models import table_influx as flux
###########add to model####################
f= flux()
serie={"tur":["FNU",[0,10],'tur','Turbidity'],"ec":['PPM',[0,500],'ec','Conductivity'],"ph":['',[0,14],'pH','ph'],"temp":['C°',[0,20],'temp','Temperature']}
f.series=serie
f.client_id=User.objects.get(username='bsens')
f.page=10
f.table='example'
f.site='B-sens_Connect'
f.save()  
############extract from model##############
""" f=User.objects.all()
for fi in f:
    print(fi)
 
fl= flux.objects.all()
i=1
for fah in fl:
    if fah.page==i:
        print(fah.site,i)"""