import socket
from threading import Thread
from Client import Client
import config
from Log import Log
import blacklist
import whitelist

class Server():
    def __init__(self):
        self.port = config.SERVER_PORT
        Log("Server starting")

    def handle(self, clientsocket, address):
        client = Client(clientsocket, address)
        client.run()

    def newClient(self, clientsocket, address):
        thread = Thread(target = self.handle, args = (clientsocket, address, ))
        thread.start()

    def run(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(("", config.SERVER_PORT))
        self.socket.listen(config.LISTEN_QUE)
        while True:
            clientsocket, address = self.socket.accept()
            if not whitelist.isWhitelisted(address[0]):
                Log(f"{address[0]}: Is not whitelisted")
                continue
            if blacklist.isBlacklisted(address[0]):
                Log(f"{address[0]}: Is blacklisted")
                continue
            self.newClient(clientsocket, address)
    
    def __del__(self):
        self.socket.close()
        Log("Server socket closed")