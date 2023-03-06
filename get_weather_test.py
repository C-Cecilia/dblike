import requests
import json
import time
import traceback

weather_url = "https://api.openweathermap.org/data/2.5/weather?q=Dublin,ie&appid=bfc1e0afba094936525c01995c2cbbc6"



def main():

    while True:
        try:

            respond = requests.get(weather_url)

            json.loads(respond.text)
            print(respond.json())
            time.sleep(5*60)
        except:

            print(traceback.format_exc())

    
    
main()