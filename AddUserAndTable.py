import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')


import json
import django
django.setup()
from django.contrib.auth.models import User
from apps.home.models import table_influx

new_table = table_influx(client_id=table_influx.objects.create(client_id_id=1),table_influx.objects.create(series={"tur": ["FNU", [0, 10], "tur", "Turbidity"]}))
#,page=4,table='Example',site='Demo 3')
new_table.save()
