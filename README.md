# Teltonika Codec 8 Server

## How it works
#### Server class
After the service starts, one instanse of the server class is called. The server will start listening at the port specifyed in the config.  

#### New Connection
If the server gets a new connection, the server will initiate a new thread with one instanse of the Client class.

#### Client
When a client has connected. It will recive an IMEI and some data, this will be sendt to the API. 

#### Closing connection
After the timeout, the client will die, and then the thread will die.

#### Loging 
Every event will be logged in the log. The log can be found in "log/year-month-day.log"

## Install
Go to the "/opt" directory. 
```
cd /opt
```
Clone the git repo
```
sudo git clone git@github.com:Vidarpettersen/teltonika-codec8-server.git
```
Start the script
```
python3 teltonika-codec8-server.py
```

## Install Service
1. Copy the service to the service folder
```
sudo cp /opt/teltonika-codec8-server/service/teltonika-codec8-server.service /etc/systemd/system/teltonika-codec8-server.service
```

2. Reload the system deamon
```
sudo systemctl daemon-reload
```

3. Enable service so it doesn't get dissabled if the server restarts
```
sudo systemctl enable teltonika-codec8-server.service
```

## Commands
#### Start service
```
sudo systemctl start teltonika-codec8-server.service
```

#### Stop service 
```
sudo systemctl stop teltonika-codec8-server.service
```

#### Restart service
```
sudo systemctl restart teltonika-codec8-server.service
```

#### Status on service
```
sudo systemctl status teltonika-codec8-server.service
```

#### Status of all services
```
systemctl --type=service
```
