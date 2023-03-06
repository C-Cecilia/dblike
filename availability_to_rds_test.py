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
    availability_json = respond.json()
    # time.sleep(5*60)
except:

    print(traceback.format_exc())



mysql_statement="INSERT INTO availability (number, last_update, available_bikes, available_bike_stands, status) VALUES"
for availability_info in availability_json:
    number = str(availability_info['number'])
    last_update = str(availability_info['last_update']/1000)
    available_bikes = str(availability_info['available_bikes'])
    available_bike_stands = str(availability_info['available_bike_stands'])
    status = "\'"+availability_info['status']+"\'"
    mysql_statement+="("+number+", "+last_update+", "+available_bikes+", "+available_bike_stands+", "+status+")"
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

engine.execute("TRUNCATE TABLE dbike.availability;")
engine.execute(mysql_statement)

