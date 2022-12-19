from django.http import HttpResponse
from django.urls import reverse
from influxdb import InfluxDBClient
from decouple import config
import os
import pandas as pd
from django.contrib.auth.models import User
from apps.home.models import table_influx
import mimetypes
import zipfile as zip
# Create your views here.

def download_to_csv(series = {"null"}, database='', start='now()-24h',end=''):
    DEFAULT_START="now()-24h"
    #safe_end = currentdatecheck(end)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    #on se connecte a la base de donnée influx
    client = InfluxDBClient(host='connect-bsens.ddns.net',
                            port=8086,
                            database=database,ssl=True,
                            username='Bsens',password=config('PASSWORD',default='password')
                            )
         
    for serie in series:
       
        if str(start) == str(DEFAULT_START):
            result = client.query("SELECT * FROM {} where time >= '{}' AND time <= '{}' ".format(series[serie][2],str(start),str(end)))
        else:
             result = client.query("SELECT * FROM {} where time >= '{}' AND time <= '{}' ".format(series[serie][2],str(start),str(end)))

        test_points = list(result.get_points(measurement=series[serie][2]))
        #print(series[serie][2])
        # Define the full file path
        filepath = BASE_DIR + '/media/' + 'data_{}.csv'.format(serie)
        df = pd.DataFrame(test_points)
        df.to_csv(filepath, index = False)
    client.close()
    
    return series

def download_multiple_file(request):
    #base de donnée materiel
    influx=table_influx.objects.all()
    #capteur=capteur_Bsens.objects.all()
    #utilisateur
    user=User.objects.all()
    msg=request.session.get('url_parameter')
    date_dl =request.POST.get('ddl-date')
    from datetime import datetime
    date_dl=date_dl.split(" - ")
    timestamp=[]
    for daty in date_dl:
       
        daty = datetime.strptime(daty,'%d/%m/%Y %H:%M')
        timestamp.append(daty)
    #series = {"Turbidity": ["FNU", [0, 500], "tur"], "Conductivity": ["PPM", [0, 500], "ec"], "pH": ["", [0, 14], "ph"], "Temperature": ["C°", [0, 20], "temp"]}
  
    for flux in influx:
            if (str)(flux.client_id) == (str)(request.user.username) and (int)(flux.page) == (int)(msg) :
                database=flux.table
                if (str)(timestamp) != '' :
                        series= download_to_csv(series = flux.series,database=database,start=timestamp[0],end=timestamp[1])
                        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                        zipfile=BASE_DIR+'/media/files.zip'
                        with zip.ZipFile(zipfile,'w')as my_zip:
                            for serie in series:
                                filename='data_{}.csv'.format(serie)
                                filepath=BASE_DIR+'/media/'+filename
                                my_zip.write(filepath,filename)
                                os.remove(filepath)
                        my_zip.close
                    
                        path = open(zipfile, 'rb')
                            # Set the mime type
                        mime_type, _ = mimetypes.guess_type(zipfile)
                            # Set the return value of the HttpResponse
                        response = HttpResponse(path,content_type=mime_type)
                            # Set the HTTP header for sending to browser
                        
                        response['Content-Disposition'] = 'attachment; filename=files_{}_{}.zip'.format(database,date_dl[0])
                        os.remove(zipfile)
                        # Return the response value
                        return response 
                else: 
                    series= download_to_csv(series = flux.series,database=database)
                    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                    zipfile=BASE_DIR+'/media/files.zip'
                    with zip.ZipFile(zipfile,'w')as my_zip:
                        for serie in series:
                            filename='data_{}.csv'.format(serie)
                            filepath=BASE_DIR+'/media/'+filename
                            my_zip.write(filepath,filename)
                            os.remove(filepath)
                        my_zip.close
                        
                    path = open(zipfile, 'rb')
                                # Set the mime type
                    mime_type, _ = mimetypes.guess_type(zipfile)
                                # Set the return value of the HttpResponse
                    response = HttpResponse(path,content_type=mime_type)
                                # Set the HTTP header for sending to browser
                            
                    response['Content-Disposition'] = 'attachment; filename=files_{}.zip'.format(database)
                    os.remove(zipfile)
                            # Return the response value
                    return response

            else:
                continue
