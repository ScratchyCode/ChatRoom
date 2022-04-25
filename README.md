# ChatRoom
![](https://img.shields.io/apm/l/vim-mode?style=plastic)
![](https://img.shields.io/pypi/pyversions/Django?style=plastic)
![](https://img.shields.io/github/last-commit/IamLucif3r/Chat-On)
![](https://img.shields.io/github/commit-activity/w/IamLucif3r/Chat-On?style=plastic)


This is an advanced Python-based chat room with secure login. The project is entirely based on the socket programming done using Python. A server is set to the listening mode, with a specific IP address and port number (asked at runtime) and clients are made to connect to the server, after which they are prompted to enter a nickname and password. The messages are then broadcasted to all the connected clients.

It is also possible to ensure traffic by wrapping TCP packet into TOR encrypted connection creating hidden service and using torsocks.

### Introduction

#### Sockets
<b> Sockets </b> and the socket API are used to send messages across a network. They provide a form of inter-process communication (IPC). The network can be a logical, local network to the computer, or one that’s physically connected to an external network, with its own connections to other networks. The obvious example is the Internet, which you connect to via your ISP. <br><br>
<img align="center" height=300px src=https://github.com/IamLucif3r/Chat-On/blob/main/assets/Python-Sockets-Tutorial_Watermarked.webp> <br>
Image Credit:[Real Python](https://realpython.com/python-sockets/)

#### TCP Socket
In the diagram below, given the sequence of socket API calls and data flow for TCP:
<br><br>
<img align="center" src=https://github.com/IamLucif3r/Chat-On/blob/main/assets/Screenshot%20at%202021-05-21%2010-47-40.png height=500px>

## Usage in clearnet

1. We will have to start our server first.
``` shell
python3 server.py
```
2. Run the client file, to start the conversation. 
``` shell
python3 client.py
```
<br>
3. enter a nickname, password and server address for start your chatting.

## Creating chat over deepweb
1. Create hidden service editing '/etc/tor/torrc' (under Linux) with:
```shell
HiddenServiceDir /var/lib/tor/ChatRoom/
HiddenServicePort 8080 127.0.0.1:8080
```

2. Restart TOR:
```shell
$ systemctl restart tor
```

3. Find onion address:
```shell
$ cat /var/lib/tor/ChatRoom/hostname
```

4. Start server.py and compile the bind entry with localhost:
```shell
 Bind address (clear for all interface): 127.0.0.1
```
With this feature we will receive only tor connections, being able to leave the ports of the firewall and the router closes.

5. Then start client.py typing:
```shell
$ torsocks python3 client.py
```
and compile entries 'Host' and 'Port' with onion address and port used before in tor setup.

## Using TOR screenshot 📹
<br>
First start server over hidden service:
<br><br>

![](https://github.com/ScratchyCode/ChatRoom/blob/main/screen/server.png)

after try to connect clients with torsocks wrapper:

![](https://github.com/ScratchyCode/ChatRoom/blob/main/screen/client.png)

<hr>
