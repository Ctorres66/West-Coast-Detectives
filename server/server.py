import socket
from _thread import *
import sys

#localhost currently (only people connected to Carlos' router can connect)
#first run server script, then run client scripts

server = "192.168.1.149"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

# 6 is the maximum player # for Clue-Less
s.listen(6)
print("Waiting for a Connection, Server Started")

def threaded_client(conn):
    reply = ""
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode("utf-8")

            if not data:
                print("Disconnected")
                break
            else:
                print("Recieved : ", reply)
                print("Sending  : ", reply)

            conn.sendall(str.encode(reply))
        except:
            break

    pass


while True:
    conn, addr = s.accept()
    print("Connected to ", addr)

    start_new_thread(threaded_client, (conn,))


