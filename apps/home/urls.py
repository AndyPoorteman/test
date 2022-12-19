# -*- encoding: utf-8 -*-


from django.urls import path, re_path
from apps.home import views
from apps.downloads.views import download_multiple_file

urlpatterns = [

    # The home page
    path('', views.index, name='home'),#page d'accueil
    path('<int:url_parameter>',views.index,name='index_dyn'),#page avec numero
    path('hello-world/',views.hello_world_view,name='hello-world'),#mise a jour graphique
    path('download/', download_multiple_file, name= 'download')#lien de telechargement
   

]
