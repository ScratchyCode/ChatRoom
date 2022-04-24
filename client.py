# Coded by Pietro Squilla
import socket
import threading
import hashlib

# input username
nickname = input("Nickname: ")

# input password
password = input("Password: ")
password = hashlib.sha256(str.encode(password)).hexdigest()

# connect to host
host = input("Host: ")
port = int(input("Port: "))

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((host,port))

stop_thread = False

def recieve():
    while True:
        global stop_thread
        if stop_thread:
            break    
        try:
            message = client.recv(1024).decode()
            if message == 'NICK':
                client.send(nickname.encode())
                next_message = client.recv(1024).decode()
                if next_message == 'PASS':
                    client.send(password.encode())
                    if(client.recv(1024).decode() == 'REFUSE'):
                        print("* Connection refused!")
                        stop_thread = True
                # clients those are banned can't reconnect
                elif next_message == 'BAN':
                    print('* Connection refused due to ban!')
                    client.close()
                    stop_thread = True
            else:
                print(message)
        except:
            print('* Error occured while connecting')
            client.close()
            break
        
def write():
    while True:
        if stop_thread:
            break
        # getting messages
        message = f'{nickname}: {input("")}'
        if message[len(nickname)+2:].startswith('/'):
            if nickname == 'admin':
                if message[len(nickname)+2:].startswith('/kick'):
                    # 2 for : and whitespace and 6 for /KICK_
                    client.send(f'KICK {message[len(nickname)+2+6:]}'.encode())
                elif message[len(nickname)+2:].startswith('/ban'):
                    # 2 for : and whitespace and 5 for /BAN
                    client.send(f'BAN {message[len(nickname)+2+5:]}'.encode())
            else:
                print("* Commands can be executed by admins only!")
        else:
            client.send(message.encode())

recieve_thread = threading.Thread(target=recieve)
recieve_thread.start()
write_thread = threading.Thread(target=write)
write_thread.start()
