# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin

# Register your models here.
from .models import table_influx,imgSociete
#ajoute des table a django admin
admin.site.register(table_influx)
admin.site.register(imgSociete)