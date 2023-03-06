import requests
import json
import time
import traceback


JCKEY = "a651416cd63f71cc1a85bdbb9c718b8b752ff9b1"
NAME = "dublin"
STATIONS_URI = "https://api.jcdecaux.com/vls/v1/stations"


def main():

    while True:
        try:

            respond = requests.get(STATIONS_URI, params={"apiKey": JCKEY, "contract": NAME})

            json.loads(respond.text)
            print(respond.json())
            time.sleep(5*60)
        except:

            print(traceback.format_exc())

        return

main()