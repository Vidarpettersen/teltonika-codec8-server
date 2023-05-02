import requests
import config
from Log import Log
import blacklist

class Client():
    def __init__(self, clientsocket, address):
        self.active = True
        self.firstRun = True
        self.imei = ""
        self.clientsocket = clientsocket
        self.address = address[0]
        self.port = address[1]
        Log(f"{str(self.address)}: New connection")
    
    def run(self):
        while self.active:
            if blacklist.isBlacklisted(self.address):
                return
            try:
                self.clientsocket.settimeout(config.SOCKET_TIMEOUT)
                data = self.clientsocket.recv(1024).decode('hex')
                print(data)
            except:
                return
        
    def sendToApi(self, data):
        try:
            json={"token": self.imei, "data": data}
            r = requests.post(config.API_ADDRESS, json=json)
            if r.status_code:
                text = r.status_code
                if r.content:
                    text = f"{text} - {r.content.decode('utf-8')}"
                if r.status_code == 200:
                    return Log(f"{str(self.address)}: {text}")
                if r.status_code == 403:
                    blacklist.add(self.address)
                    return Log(f"{str(self.address)}: {text}")
                if r.status_code == 406:
                    Log(f"{str(self.address)}: {text}")
                    self.active = False
                    return 
                if r.status_code == 429:
                    return Log(f"{str(self.address)}: 429 - Too Many Requests")
                
                if r.status_code == 500:
                    return Log(f"{str(self.address)}: 500 - Server Error")
                
                Log(f"{str(self.address)}: {r.status_code} - Ukjent feilmelding")
        except:
            Log(f"{str(self.address)}: 404")

    def __del__(self):
        Log(f"{str(self.address)}: Connection closed")
        self.clientsocket.close()