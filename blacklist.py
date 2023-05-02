import config
from datetime import datetime

def timestamp():
    dt = datetime.now()
    ts = datetime.timestamp(dt)
    return ts

blacklist = {}

def get():
    global blacklist
    return blacklist

def load():
    global blacklist
    try:
        with open(config.BLACKLIST_FILE, 'r') as f:
            for line in f:
                items = line.split()
                key, values = items[0], items[1:][0]
                blacklist[key] = values
    except:
        return

def save():
    global blacklist
    with open(config.BLACKLIST_FILE, 'w') as f:
        for key, value in blacklist.items(): 
            f.write('%s %s\n' % (key, value))

def add(ip):
    global blacklist
    if not ip in blacklist or float(blacklist[ip]) < timestamp():
        blacklist[ip] = timestamp() + (config.BLACKLIST_TIME * 60)
        save()      

def isBlacklisted(ip):
    global blacklist
    if ip in blacklist:
        if float(blacklist[ip]) > timestamp():
            return True
    return False