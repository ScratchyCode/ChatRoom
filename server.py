# Coded by Pietro Squilla
import threading
import socket

host = ''
port = int(input("Listening port: "))

# list to contain the clients getting connected and nicknames
clients = []
nicknames = []
hashTable = {}


# broadcasting method
def broadcast(message):
    try:
        for client in clients:
            client.send(message)
    except:
        client.close()


# recieving messages from client then broadcasting
def handle(client):
    while True:
        try:
            msg = message = client.recv(1024)
            
            if(not msg):
                broadcast(f"* '{nickname}' quit.".encode())
                print(f"'%s' disconnected." %nickname)
                index = clients.index(client)
                # index is used to remove client from list after getting disconnected
                clients.remove(client)
                nickname = nicknames[index]
                nicknames.remove(nickname)
                client.close
                break
            
            if msg.decode( ).startswith("KICK"):
                if nicknames[clients.index(client)] == "admin":
                    name_to_kick = msg.decode( )[5:]
                    kick_user(name_to_kick)
                else:
                    client.send("* Command refused!".encode( ))
            elif msg.decode( ).startswith("BAN"):
                if nicknames[clients.index(client)] == "admin":
                    name_to_ban = msg.decode( )[4:]
                    kick_user(name_to_ban)
                    with open("bans.txt",'a') as f:
                        f.write(f"{name_to_ban}\n")
                    print(f"* {name_to_ban} was banned by the admin!")
                else:
                    client.send("* Command refused!".encode( ))
            else:
                broadcast(message) # as soon as message recieved, broadcast it.
        except:
            if client in clients:
                index = clients.index(client)
                # index is used to remove client from list after getting disconnected
                clients.remove(client)
                client.close
                nickname = nicknames[index]
                broadcast(f"* '{nickname}' left.".encode( ))
                print(f"'%s' disconnected." %nickname)
                nicknames.remove(nickname)
                break


# main
def main():
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((host,port))
    server.listen(5)
    
    while True:
        client,address = server.accept()
        
        print(f"* Connected with {str(address)}")
        
        # ask the clients for nicknames
        client.send("NICK".encode( ))
        nickname = client.recv(1024).decode( )
        
        # check for banned nick
        with open("bans.txt",'r') as f:
            bans = f.readlines()
        
        if nickname+'\n' in bans:
            client.send("BAN".encode( ))
            client.close()
            continue
        
        # ask the passwd
        client.send("PASS".encode( ))
        password = client.recv(1024).decode( )
        
        # REGISTERATION PHASE
        # if new user, regiter in hashTable dictionary
        if nickname not in hashTable:
            hashTable[nickname] = password
            #client.send(str.encode("Signup successful.")) 
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
        
        #print(f'Nickname of the client is {nickname}')
        broadcast(f"* {nickname} joined the server".encode( ))
        client.send(f"* Connected to the server!".encode( ))
        
        # handling multiple clients simultaneously
        thread = threading.Thread(target=handle,args=(client,))
        thread.start()


def kick_user(name):
    if name in nicknames:
        name_index = nicknames.index(name)
        client_to_kick = clients[name_index]
        clients.remove(client_to_kick)
        client_to_kick.send("* You were kicked from the server!".encode( ))
        client_to_kick.close()
        nicknames.remove(name)
        broadcast(f"* {name} was kicked from the server!".encode( ))


##############
#    main    #
##############
if(__name__ == "__main__"):
    
    print("Starting server...")
    main()
    
