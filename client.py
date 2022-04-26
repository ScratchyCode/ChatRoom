# Coded by Pietro Squilla
import socket
import threading
import hashlib

# dim buffer for messages
BUFF = 2048

# for nickname
class coloritesto:
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"

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

# threaded function for tx and rx
def rx():
    while True:
        global stop_thread
        if stop_thread:
            break    
        try:
            message = client.recv(BUFF).decode()
            if(not message):
                print("* Server connection lost.")
                stop_thread = True
                client.close()
                break
            
            if message == 'NICK':
                client.send(nickname.encode())
                next_message = client.recv(BUFF).decode()
                if next_message == 'PASS':
                    client.send(password.encode())
                    if(client.recv(BUFF).decode() == 'REFUSE'):
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


def tx():
    while True:
        if stop_thread:
            break
        # getting messages
        #message = f'{nickname}: {input("")}'
        message = f'{nickname}'
        message = coloritesto.RED + coloritesto.BOLD + message + coloritesto.END
        message = message + f': {input("")}'
        
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


# start thread
recieve_thread = threading.Thread(target=rx)
recieve_thread.start()
write_thread = threading.Thread(target=tx)
write_thread.start()
