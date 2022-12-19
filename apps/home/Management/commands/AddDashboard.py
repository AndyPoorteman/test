import os
import django
os.environ.setdefault('DJANGO_SETTING_MODULE', 'core.settings')
django.setup()
#from django.core.managemen.base import BaseCommand, CommandError
from home.model import table_influx as flux

""" class Command(BaseComand):
    help = ' Close the specified poll for voting'

    def add_arguments(self,parser):
        parser.add_argument('poll_ids', nargs='+',type=int)

    def handle(self,*args,**options):
        for poll_id  in options['poll_ids']:
            try:
                poll= flux.objects.create()
                poll.client_id='Bsens'
                poll.series={"tur":["FNU",[0,10],'tur','Turbidity'],"ec":['PPM',[0,500],'ec','Conductivity'],"ph":['',[0,14],'pH','ph'],"temp":['C°',[0,20],'temp','Temperature']}
                poll.page = 4
                poll.table = "Example"
                poll.site="titre"
                poll.save()
                self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id)) """
serie={"tur":["FNU",[0,10],'tur','Turbidity'],"ec":['PPM',[0,500],'ec','Conductivity'],"ph":['',[0,14],'pH','ph'],"temp":['C°',[0,20],'temp','Temperature']}
new_flux=flux(client_id.id==1,series=serie,page=3,table ='example',site='script')
new_flux.save()