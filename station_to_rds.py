import requests
import json
import time
import traceback
import sqlalchemy
from sqlalchemy import create_engine
import traceback
import glob
import os
from pprint import pprint
import simplejson
from IPython.display import display


JCKEY = "a651416cd63f71cc1a85bdbb9c718b8b752ff9b1"
NAME = "dublin"
STATIONS_URI = "https://api.jcdecaux.com/vls/v1/stations"
try:

    respond = requests.get(STATIONS_URI, params={
                           "apiKey": JCKEY, "contract": NAME})

    json.loads(respond.text)
    station_json = respond.json()
    # time.sleep(5*60)
except:

    print(traceback.format_exc())

# print(len(station_json))


mysql_statement="INSERT INTO station (number, address, banking, bike_stands, name, position_lat, position_lng) VALUES"
for station_info in station_json:
    number = str(station_info['number'])
    address = "\'"+station_info['address'].replace("'","\\'")+"\'"
    banking = str(station_info['banking'])
    bike_stands = str(station_info['bike_stands'])
    name = "\'"+station_info['name'].replace("'","\\'")+"\'"
    position_lat = str(station_info['position']['lat'])
    position_lng = str(station_info['position']['lng'])
    mysql_statement+="("+number+", "+address+", "+banking+", "+bike_stands+", "+name+", "+position_lat+", "+position_lng+")"
    mysql_statement+=", "

mysql_statement = mysql_statement[:-2] + ";"
# print(mysql_statement)


URL = "dbbike.ck6m6unryigy.us-east-1.rds.amazonaws.com"
PORT = "3306"
DB = "dbike"
USER = "admin"
PASSWORD = "DBbike30830"


engine = create_engine(
    ("mysql+mysqldb://{}:{}@{}:{}/{}").format(USER, PASSWORD, URL, PORT, DB), echo=True)

engine.execute("TRUNCATE TABLE dbike.station;")
engine.execute(mysql_statement)

