import config
from datetime import datetime

def timestamp():
    dt = datetime.now()
    ts = datetime.timestamp(dt)
    return ts

whitelist = {}

def get():
    global whitelist
    return whitelist

def load():
    global whitelist
    try:
        with open(config.WHITELIST_FILE, 'r') as f:
            for line in f:
                line = line.split('\n')[0]
                whitelist[line] = line.split('.')
    except:
        return

def isWhitelisted(ip):
    global whitelist
    splitted = ip.split('.')
    for ip in whitelist:
        whiteip = ip.split('.')
        if splitted[0] != whiteip[0] and whiteip[0] != 'x':
            continue
        if splitted[1] != whiteip[1] and whiteip[1] != 'x':
            continue
        if splitted[2] != whiteip[2] and whiteip[2] != 'x':
            continue
        if splitted[3] != whiteip[3] and whiteip[3] != 'x':
            continue
        return True
    return False