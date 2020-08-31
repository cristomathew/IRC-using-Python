import socket
import threading
import time
#COLOR CODES
OKBLUE = '\033[94m'
OKYELLOW = '\033[93m'
OKGREEN = '\033[92m'
OKRED = '\033[91m'
BOLD = '\033[1m'
ENDC = '\033[0m'




HEADER = 64
PORT = 6450
SERVER = '171.49.181.4'
DISCONNECT_MSG = '#DISCONNECT'

ADDR = (SERVER,PORT)
FORMAT = 'utf-8'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)



def msg_check():
    while True:
        try:
            message = client.recv(2048).decode(FORMAT)
            print(OKBLUE+message+ENDC)
        except KeyboardInterrupt:
            break
def send_msg(msg):
    msg = username+"::"+msg
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length+=b' '*(HEADER-len(send_length))
    client.send(send_length)
    client.send(message)


username = input(OKYELLOW+"Enter a username:"+ENDC)
send_msg(username)
user_result = client.recv(2048).decode(FORMAT)
if user_result == "False":
    print(OKRED+BOLD+f"User account with {username} was not found"+ENDC)
    print(OKYELLOW+"Creating new account with above username"+ENDC)
    password = input(OKGREEN+"Enter new password: "+ENDC)
    password = username+"::"+password
    send_msg(password)
    result = client.recv(2048).decode(FORMAT)
    if result == "True":
        print(OKGREEN+"User has been successfully added"+ENDC+OKYELLOW+"Restart program"+ENDC)
        send_msg(DISCONNECT_MSG)
    else:
        print(OKRED+"Unable to add user please try again later...")
        send_msg(DISCONNECT_MSG)
else:
    password = input("Enter password: ")
    if user_result == password:
        text_msg = "Logged in to the Server"
        for text in text_msg:
            print(OKBLUE+text+ENDC,end='',flush=True)
            time.sleep(0.04)
        print("\n")
        def client_main():
            connected = True
            send_msg("has Joined Server")
            text_msg = "To send a message press control+C"
            for text in text_msg:
                print(OKRED+BOLD+text+ENDC,end='',flush=True)
                time.sleep(0.04)
            print("\n")
            while connected:
                try:
                    msg_check()
                    print("\n")
                    message = input(OKGREEN+"MSG: "+ENDC)
                    if message == 'disconnect':
                        connected = False
                        break
                    send_msg(message)
                except KeyboardInterrupt:
                    connected = False
                    break
            send_msg(DISCONNECT_MSG)
        send_msg("has Joined Server")
        client_main()
    else:
        print(OKRED+"Wrong Password"+ENDC)
        send_msg(DISCONNECT_MSG)