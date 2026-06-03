import requests
import config
from Log import Log
import blacklist
from TeltonikaCodec8Decoder.decoder import Decoder
import codecs

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
                data = self.clientsocket.recv(1024)
                
                if not data:
                    # Connection closed by client
                    return
                
                data_hex = data.hex()
                
                if self.imei == "":
                    # First 2 bytes (4 hex chars) are the IMEI length, skip them
                    imei_data = data_hex[4:]  # Skip length prefix
                    self.imei = codecs.decode(imei_data, 'hex').decode('ascii')
                    # Send acceptance acknowledgment (0x01) after receiving IMEI
                    self.clientsocket.send(bytes.fromhex('01'))
                    Log(f"{str(self.address)}: IMEI accepted: {self.imei}")
                    continue
                
                # AVL data packet received
                Log(f"{str(self.address)}: Received {len(data)} bytes of AVL data")
                decoder = Decoder()
                decoder.decode(data_hex)
                records = list(decoder.toJson())
                record_count = len(records)
                
                # Send number of records received as 4-byte integer (big-endian)
                response = record_count.to_bytes(4, byteorder='big')
                self.clientsocket.send(response)
                Log(f"{str(self.address)}: Acknowledged {record_count} records")
                
                for json in records:
                    #print(json)
                    self.sendToApi(json)
            except Exception as e:
                Log(f"{str(self.address)}: Error - {str(e)}")
                return
        

        
    def sendToApi(self, data):
        json={"token": self.imei, "data": data }
        try:
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