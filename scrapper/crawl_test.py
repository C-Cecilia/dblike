import config
import requests
import json
import datetime
import time
import traceback
from sqlalchemy import create_engine
from sqlalchemy import text
import traceback
import glob
import os
from pprint import pprint
import simplejson
from IPython.display import display
import os


def write_availability_to_db(respond_json):

    mysql_statement = "INSERT INTO availability (number, last_update, available_bikes, available_bike_stands, status) VALUES"
    for availability_info in respond_json:
        number = str(availability_info['number'])
        last_update = str(availability_info['last_update']/1000)
        available_bikes = str(availability_info['available_bikes'])
        available_bike_stands = str(availability_info['available_bike_stands'])
        status = "\'"+availability_info['status']+"\'"
        mysql_statement += "("+number+", "+last_update+", " + \
            available_bikes+", "+available_bike_stands+", "+status+")"
        mysql_statement += ", "

    mysql_statement = mysql_statement[:-2] + ";"

    engine = create_engine(
        ("mysql+mysqldb://{}:{}@{}:{}/{}").format(config.USER, config.PASSWORD, config.URL, config.PORT, config.DB), echo=True)
    
    with engine.connect() as connection:

        # connection.execute("TRUNCATE TABLE dbike.availability;")
        connection.execute(mysql_statement)


def write_availability_to_file(text, now):
    directory = "static/bikeData"
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open("static/bikeData/bike_{}".format(now).replace(" ", "_"), 'w') as f:
        f.write(text)
    


def write_station_to_db(respond_json):

    mysql_statement = "INSERT INTO station (number, address, banking, bike_stands, name, position_lat, position_lng) VALUES"
    for station_info in respond_json:
        number = str(station_info['number'])
        address = "\'"+station_info['address'].replace("'", "\\'")+"\'"
        banking = str(station_info['banking'])
        bike_stands = str(station_info['bike_stands'])
        name = "\'"+station_info['name'].replace("'", "\\'")+"\'"
        position_lat = str(station_info['position']['lat'])
        position_lng = str(station_info['position']['lng'])
        mysql_statement += "("+number+", "+address+", "+banking+", " + \
            bike_stands+", "+name+", "+position_lat+", "+position_lng+")"
        mysql_statement += ", "

    mysql_statement = mysql_statement[:-2] + ";"

    engine = create_engine(
        ("mysql+mysqldb://{}:{}@{}:{}/{}").format(config.USER, config.PASSWORD, config.URL, config.PORT, config.DB), echo=True)
    
    with engine.connect() as connection:

        # connection.execute("TRUNCATE TABLE dbike.station;")
        connection.execute(text(mysql_statement))


def write_weather_to_db(weather_json):
    time = str(weather_json['dt'])
    main_weather = "\'"+weather_json['weather'][0]['main']+"\'"
    visibility = str(weather_json['visibility'])
    wind_speed = str(weather_json['wind']['speed'])
    temp = str(weather_json['main']['temp']-273.15)
    humidity = str(weather_json['main']['humidity'])

    engine = create_engine(
        ("mysql+mysqldb://{}:{}@{}:{}/{}").format(config.USER, config.PASSWORD, config.URL, config.PORT, config.DB), echo=True)
    
   
    with engine.connect() as connection:
         # connection.execute("TRUNCATE TABLE dbike.weather;")
       query = "INSERT INTO weather (time, main_weather, visibility, wind_speed, temp, humidity) VALUES ("+time+", "+main_weather+", "+visibility+", "+wind_speed+", "+temp+", "+humidity+");"
       connection.execute(text(query))



def write_weather_to_file(text, now):
    with open("static/weatherData/weather_{}".format(now).replace(" ", "_"), 'w')as f:
        f.write(text)


def availability():
    
    # while True:
        try:
            now = datetime.datetime.now()
            respond = requests.get(config.STATIONS_URI, params={
                "apiKey": config.JCKEY, "contract": config.NAME})
            print(respond, now)
            write_availability_to_file(respond.text, now)
            write_availability_to_db(respond.json())
            time.sleep(5*60)

        except:
            print(traceback.format_exc())
        # return

def station():
    try:
        respond = requests.get(config.STATIONS_URI, params={
            "apiKey": config.JCKEY, "contract": config.NAME})
        json.loads(respond.text)
        write_station_to_db(respond.json())
        # time.sleep(5*60)
    except:
        print(traceback.format_exc())


def weather():
    # while True:
        try:
            now = datetime.datetime.now()
            respond = requests.get(
                "https://api.openweathermap.org/data/2.5/weather?q=Dublin,ie&appid=bfc1e0afba094936525c01995c2cbbc6")

            json.loads(respond.text)
            write_weather_to_db(respond.json())
            write_weather_to_file(respond.text, now)
            time.sleep(60*60)
        except:
            print(traceback.format_exc())
        # return

availability()
weather()
station()
