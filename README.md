# ChatRoom
This is an advanced Python-based chat room with secure login. The project is entirely based on the socket programming done using Python. The server is set to the listening mode, with a specific port number (asked at runtime). Client are made to connect to the server, prompted to enter a nickname and password. The messages are then broadcasted to all the connected clients.

First login will register nickname and password on the server.

It is also possible to ensure traffic by wrapping TCP packet into TOR full-encrypted connection, creating hidden service and using torsocks.

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

## Chatting over deep web
1. Install TOR typing (under Linux):
```shell
sudo apt install tor
```

2. Create hidden service editing '/etc/tor/torrc' with:
```shell
HiddenServiceDir /var/lib/tor/ChatRoom/
HiddenServicePort 8080 127.0.0.1:8080
```

3. Restart TOR:
```shell
$ systemctl restart tor
```

4. Find onion address:
```shell
$ cat /var/lib/tor/ChatRoom/hostname
```

5. Start server.py entering the port;

binding host = '127.0.0.1' by editing server code, we will receive only tor connections, being able to leave the ports of the firewall and the router closes.

6. Then start client.py typing:
```shell
$ torsocks python3 client.py
```
and compile entries 'Host' and 'Port' with onion address and port (8080) used before in tor setup.

## Example of TOR connection
<br>
Server-side:
<br><br>

![](https://github.com/ScratchyCode/ChatRoom/blob/main/screenshot/server1.png)

Client-side:

![](https://github.com/ScratchyCode/ChatRoom/blob/main/screenshot/client1.png)

<hr>
