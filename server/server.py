import socket
import threading
import pickle
from users import Users

HEADER = 64
PORT = 6450
SERVER = '192.168.1.5'

ADDR = (SERVER,PORT)
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

client_list = []

def check_user(username):
    try:
        file_name = username+'.pkl'
        with open(file_name,'rb') as user_file:
            user = pickle.load(user_file)
            return user
    except FileNotFoundError:
        return False

def add_user(user):
    file_name = user.username + '.pkl'
    try:
        with open(file_name,'wb') as user_file:
            pickle.dump(user,user_file,pickle.HIGHEST_PROTOCOL)
            return True
    except:
        return False

def remove_client(client):
    if client in client_list:
        client_list.remove(client)

def broadcast_msg(message, connection):
    for client in client_list:
        if client != connection:
            try:
                client.send(message.encode(FORMAT))
            except:
                remove_client(client)

def incoming_clients(conn, addr):
    print(f"New connection established for {addr}")
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            msglist = msg.split("::")
            username,msg = msglist[0],msglist[1]
            if username == msg:
                if len(msglist) == 3:
                    username,password = msglist[1],msglist[2]
                    new_user = Users(username, password)
                    result = add_user(new_user)
                    if result:
                        conn.send("True".encode(FORMAT))
                    else:
                        conn.send("False".encode(FORMAT))
                else:
                    user = check_user(username)
                    if user:
                        password = user.password
                        conn.send(password.encode(FORMAT))
                    else:
                        conn.send("False".encode(FORMAT))
            else:
                print(f"{addr} sent: {msg}")
                conn.send("MSG RECIEVED BY THE SERVER".encode(FORMAT))
                if msg == "#DISCONNECT":
                    connected = False
                message = "<"+username+">:"+msg
                broadcast_msg(message, conn)

    conn.close()


def main():
    server.listen()
    print(f'Server has started listening for clients on {SERVER}...')
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=incoming_clients,args=(conn, addr))
        client_list.append(conn)
        thread.start()
        print(f'No of Clients that are connected: {threading.activeCount() -1}')
    server.close()

print("Server Program has started..")
main()