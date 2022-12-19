import os
import sys
import django
#print(sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "core")))
print(os.path.dirname(os.path.abspath(__file__)))
#os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'
#os.environ.setdefault('DJANGO_SETTING_MODULE', 'core.settings')
#django.setup()
""" from apps.home.model import table_influx as flux
serie={"tur":["FNU",[0,10],'tur','Turbidity'],"ec":['PPM',[0,500],'ec','Conductivity'],"ph":['',[0,14],'pH','ph'],"temp":['C°',[0,20],'temp','Temperature']}
new_flux=flux(client_id.id==1,series=serie,page=3,table ='example',site='scripting')
new_flux.save() """