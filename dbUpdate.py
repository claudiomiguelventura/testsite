import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testsite.settings")

import django
django.setup()

from django.core.management import call_command

import csv
import urllib.request
from urllib.error import HTTPError
import codecs
import dbUpdateVars as dbVars
from main.models import RainTable, RainDay
import time
# Cria concelhos e distritos como rainTables
"""for distrito in dbVars.distritos:
    for concelho in dbVars.distritos[str(distrito)]:
        codigo = dbVars.distritos[str(distrito)][str(concelho)]
        #print("Distrito: "+distrito)
        #print("- - - - Concelho: "+concelho)
        #print("- - - - - - - - Codigo: "+codigo)

        try:
            rt = RainTable.objects.get(county=concelho)
        except RainTable.DoesNotExist:
            print("County "+concelho+" was not found.")
            print("Create this county "+concelho)
            rt = RainTable(district=distrito, county=concelho, county_code=codigo)
            rt.save()
        else:
            print("County "+concelho+" sucessfully found.")
            print("Not creating it.")
        finally:
            print()"""




""" data = []

url = "https://api.ipma.pt/open-data/observation/climate/precipitation-total/"+distrito+"/mrrto-"+dico+"-"+concelho+".csv"
try:
    ftpstream = urllib.request.urlopen(url)
    csvfile = csv.reader(codecs.iterdecode(ftpstream, 'utf-8'))
    for line in csvfile:
        print(line)
        data.append(line)
except (RuntimeError, TypeError, NameError, HTTPError):
    print(HTTPError)

print("Last line should be: ")
print (data[int(len(data)-1)]) """

for distrito in dbVars.distritos:
    for concelho in dbVars.distritos[str(distrito)]:
        codigo = dbVars.distritos[str(distrito)][str(concelho)]
        print("Getting data for:")
        print("Distrito: "+distrito)
        print("- - - - Concelho: "+concelho)
        print("- - - - - - - - Codigo: "+codigo)
        
        data = []
        url = "https://api.ipma.pt/open-data/observation/climate/precipitation-total/"+distrito+"/mrrto-"+codigo+"-"+concelho+".csv"
        try:
            ftpstream = urllib.request.urlopen(url)
            csvfile = csv.reader(codecs.iterdecode(ftpstream, 'utf-8'))
            for line in csvfile:
                #print(line)
                data.append(line)
            data.pop(0)
            print("- - - - - - - - - - - - Data downloaded sucessfuly.")
        except (RuntimeError, TypeError, NameError, HTTPError):
            print(HTTPError)
        else:
            #print("Last line should be: ")
            #print("Data from: "+url)
            #print(concelho)
            #print (data[int(len(data)-1)])
            print("- - - - - - - - - - - - Processing data and updating...")
            for item in data:
                m_str = str(item)
                m_str = m_str.replace('[', '')
                m_str = m_str.replace(']', '')
                m_str = m_str.replace('\'', '')
                splitStr = m_str.split(", ")

                s_date = splitStr[0]
                s_minimum = splitStr[1]
                s_maximum = splitStr[2]
                s_range = splitStr[3]
                s_mean = splitStr[4]
                s_std = splitStr[5]

                #print("For %s we have date %s min %s max %s range %s mean %s std %s"%(concelho,s_date,s_minimum,s_maximum,s_range,s_mean,s_std))
                try:
                    rt = RainTable.objects.get(county=concelho)
                except RainTable.DoesNotExist:
                    print("- - - - - - - - - - - - County "+concelho+" was not found.")
                    print("- - - - - - - - - - - - Creating this county "+concelho)
                    rt = RainTable(district=distrito, county=concelho, county_code=codigo)
                    rt.save()
                else:
                    try:
                        #print(s_date)
                        rd = rt.rainday_set.get(rd_date=s_date)
                    except RainDay.DoesNotExist:
                        print("- - - - - - - - - - - - Rain day does not exist")
                        print("- - - - - - - - - - - - Create this rain day "+s_date)
                        rt.rainday_set.create(rd_date=s_date, rd_minimum=s_minimum, rd_maximum=s_maximum, rd_range=s_range,rd_mean=s_mean, rd_std=s_std)
                    else:
                        pass
                        #print("Rain day %s already exists for county %s disctrict %s" %(s_date, concelho, distrito))
                        #print("Do not create rainday")
                    pass
                    #print("County "+concelho+" sucessfully found.")
                    #print("Not creating it.")
                finally:
                    pass
            print("- - - - - - - - - - - - Data processing and update ended.")

            time.sleep(2.0)
        