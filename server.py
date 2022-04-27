# Coded by Pietro Squilla
import threading
import socket
import signal
import sys

#host = input("Bind address (clear for all interface): ")
host = ''
port = int(input("Listening port: "))

# dim buffer for messages
BUFF = 2048

# list to contain the clients getting connected and nicknames
clients = []
nicknames = []
hashTable = {}


# handle signal
def signal_handler(signal,frame):
    print("\nExit...")
    sys.exit(0)


# broadcasting method
def broadcast(message,myclient):
    for client in clients:
        # broadcast without echo for same client
        if(client == myclient):
            continue
        else:
            client.send(message)


# receiving messages from client then broadcasting
def handle(client):
    while True:
        try:
            msg = message = client.recv(BUFF)
            if(not msg):
                broadcast(f"* '{nickname}' quit.".encode(),client)
                print(f"'%s' disconnected." %nickname)
                index = clients.index(client)
                # index is used to remove client from list after getting disconnected
                clients.remove(client)
                nickname = nicknames[index]
                nicknames.remove(nickname)
                client.close
                break
            
            # check for command
            if(msg.decode( ).startswith("KICK")):
                if(nicknames[clients.index(client)] == "admin"):
                    name_to_kick = msg.decode( )[5:]
                    kick_user(name_to_kick)
                else:
                    client.send("* Command refused!".encode( ))
            elif(msg.decode( ).startswith("BAN")):
                if(nicknames[clients.index(client)] == "admin"):
                    name_to_ban = msg.decode( )[4:]
                    kick_user(name_to_ban)
                    with open("bans.txt",'a') as f:
                        f.write(f"{name_to_ban}\n")
                    print(f"* {name_to_ban} was banned by the admin!")
                else:
                    client.send("* Command refused!".encode( ))
            else:
                broadcast(message,client) # as soon as message received, broadcast it.
        except:
            if(client in clients):
                index = clients.index(client)
                # index is used to remove client from list after getting disconnected
                clients.remove(client)
                nickname = nicknames[index]
                broadcast(f"* '{nickname}' left.".encode( ),client)
                client.close
                print(f"'%s' disconnected." %nickname)
                nicknames.remove(nickname)
                break
            else:
                client.close
                print(f"Handshake problem with client.")
                print(f"Disconnected.")
                break


# main
def main():
    try:
        server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server.bind((host,port))
        server.listen(5)
        
        while True:
            client,address = server.accept()
            
            print(f"* Connected from {str(address)}")
            
            # ask nicknames
            try:
                client.send("NICK".encode())
                nickname = client.recv(BUFF).decode()
                
                # check connection for real user
                if(not nickname):
                    client.close
                    print(f"Disconnection client %s: handshake problem." %address[0])
                    continue
            except:
                client.close
                print(f"Disconnection client %s: handshake problem." %address[0])
                continue
            
            # check for banned nick
            with open("bans.txt",'r') as f:
                bans = f.readlines()
            
            if(nickname+'\n' in bans):
                client.send("BAN".encode( ))
                client.close()
                continue
            
            # ask passwd
            try:
                client.send("PASS".encode())
                password = client.recv(BUFF).decode()
                
                # check connection for real user
                if(not password):
                    client.close
                    print(f"Disconnection client %s: handshake problem." %address[0])
                    continue
            except:
                client.close
                print(f"Disconnection client %s: handshake problem." %address[0])
                continue
            
            # REGISTERATION PHASE
            # if new user, register in hashTable dictionary
            if(nickname not in hashTable):
                hashTable[nickname] = password
                client.send(str.encode(f"Signup successful.")) 
                print("Registered:")
                print("{:<8} {:<20}".format("User","Passwd"))
                for i,j in hashTable.items():
                    label,num = i,j
                    print("{:<8} {:<20}".format(label,num))
                print("-------------------------------------------")
            else:
                # if already existing user, check if the entered password is correct
                if(hashTable[nickname] == password):
                    client.send(str.encode("Connected...")) 
                    print("Connected user: ",nickname)
                else:
                    client.send("REFUSE".encode( ))
                    print("* Connection refused for: ",nickname)
                    client.close()
                    continue
            
            nicknames.append(nickname)
            clients.append(client)
            
            broadcast(f"* {nickname} joined the chat".encode(),client)
            client.send(f"* Connected to the server!\n".encode())
            
            # handling multiple clients simultaneously
            thread = threading.Thread(target=handle,args=(client,))
            thread.daemon = True
            thread.start()
            thread.join()
    except:
        print("Connection failure.")


def kick_user(name):
    if(name in nicknames):
        name_index = nicknames.index(name)
        client_to_kick = clients[name_index]
        clients.remove(client_to_kick)
        client_to_kick.send("* You were kicked from the server!".encode( ))
        client_to_kick.close()
        nicknames.remove(name)
        broadcast(f"* {name} was kicked from the server!".encode( ),client)


##############
#    main    #
##############
if(__name__ == "__main__"):
    # handle interrupt signal
    signal.signal(signal.SIGINT,signal_handler)
    
    print("Starting server...")
    main()
