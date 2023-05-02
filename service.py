import signal
import sys
from Server import Server
from Log import Log
import blacklist
import whitelist

def exithandler(signum, frame):
    global server
    del server
    Log("Force quit by admin")
    sys.exit(1)  # only 0 means "ok"

signal.signal(signal.SIGINT, exithandler)
signal.signal(signal.SIGTERM, exithandler)
signal.signal(signal.SIGHUP, exithandler)


blacklist.load()
whitelist.load()

server = Server()
server.run()