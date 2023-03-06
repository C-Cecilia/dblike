import requests
import json

#change the parameter below to change data request 
def main():
    
    while True:
        try:

            query="https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=a651416cd63f71cc1a85bdbb9c718b8b752ff9b1"

            getreq=requests.get(query)
            
            store(json.loads(getreq.text))
            
            time.sleep(5*60)
        except:
            
            print (traceback.format_exc())
            
        return        

print(getreq.json())



#do not need this line below 
#json.loads(getreq.text)


