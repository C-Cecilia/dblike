import requests
import json
import traceback
import sqlalchemy
from sqlalchemy import create_engine
import traceback
import glob
import os
from pprint import pprint
import simplejson
from IPython.display import display


try:

    respond = requests.get(
        "https://api.openweathermap.org/data/2.5/weather?q=Dublin,ie&appid=bfc1e0afba094936525c01995c2cbbc6")

    json.loads(respond.text)
    weather_json = respond.json()
    # time.sleep(5*60)
    # print(weather_json)
except:

    print(traceback.format_exc())


time = str(weather_json['dt'])
main_weather = "\'"+weather_json['weather'][0]['main']+"\'"
visibility = str(weather_json['visibility'])
wind_speed = str(weather_json['wind']['speed'])
temp = str(weather_json['main']['temp']-273.15)
humidity = str(weather_json['main']['humidity'])
# print(main_weather)


URL = "dbbike.c2pot9zcoud2.eu-west-1.rds.amazonaws.com"
PORT = "3306"
DB = "dbbike"
USER = "admin"
PASSWORD = "DBbike30830"

engine = create_engine(
    ("mysql+mysqldb://{}:{}@{}:{}/{}").format(USER, PASSWORD, URL, PORT, DB), echo=True)

engine.execute("INSERT INTO weather (time, main_weather, visibility, wind_speed, temp, humidity) VALUES (" +
               time+", "+main_weather+", "+visibility+", "+wind_speed+", "+temp+", "+humidity+");")
