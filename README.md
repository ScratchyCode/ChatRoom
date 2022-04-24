# ChatRoom 🐍 
![](https://img.shields.io/apm/l/vim-mode?style=plastic)
![](https://img.shields.io/pypi/pyversions/Django?style=plastic)
![](https://img.shields.io/github/last-commit/IamLucif3r/Chat-On)
![](https://img.shields.io/github/commit-activity/w/IamLucif3r/Chat-On?style=plastic)


This is an advanced Python-based chat room with secure login. The project is entirely based on the socket programming done using Python. A server is set to the listening mode, with a specific IP address and port number (asked at runtime) and clients are made to connect to the server, after which they are prompted to enter a nickname and password. The messages are then broadcasted to all the connected clients. 

### 👉 Introduction

#### 👉 Sockets
<b> Sockets </b> and the socket API are used to send messages across a network. They provide a form of inter-process communication (IPC). The network can be a logical, local network to the computer, or one that’s physically connected to an external network, with its own connections to other networks. The obvious example is the Internet, which you connect to via your ISP. <br><br>
<img align="center" height=300px src=https://github.com/IamLucif3r/Chat-On/blob/main/assets/Python-Sockets-Tutorial_Watermarked.webp> <br>
Image Credit:[Real Python](https://realpython.com/python-sockets/)

#### 👉 TCP Socket
In the diagram below, given the sequence of socket API calls and data flow for TCP:
<br><br>
<img align="center" src=https://github.com/IamLucif3r/Chat-On/blob/main/assets/Screenshot%20at%202021-05-21%2010-47-40.png height=500px>

## 👉 Usage

1. We will have to start our server first.
``` shell
python server.py
```
2. Run the client file, to start the conversation. 
``` Shell
python client.py
```
<br>
3. enter a nickname, password and start your chatting. 


## v1.2 Updates
- The version 1.2 supports the Admin Controls. The admin has certain controls over the chat room.
- The enhanced features include
  - <b>Kick Feature</b> : Admin can kick anyone from the Chat Room.
  - <b>Ban Feature</b> : Admin can ban certain members from re-joining the Chat Room. These names are added in a List.
- Minor Bug Fixes.

<hr>

## Demo-Video 📹
<br>
This is a demo video of the working of main-forked project.
This fork work similarly.
<br><br>

![](https://github.com/IamLucif3r/Chat-On/blob/main/assets/2021-05-22-15-10-08.gif)

<hr>
