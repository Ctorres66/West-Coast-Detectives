import socket
from _thread import *
from constants import *
import sys

#localhost currently (only people connected to Carlos' router can connect)
#first run server script, then run client scripts

#server value must be your wifis ipv4 address
server = "172.16.0.13"
port = 5555
max_players = MAX_PLAYERS

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

# 6 is the maximum player # for Clue-Less
s.listen(max_players)
print("Waiting for a Connection, Server Started")


def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])


def make_pos(tup):
    return str(tup[0]) + " , " + str(tup[1])


pos = [(0,0), (100,100)]


def threaded_client(conn, player):
    conn.send(str.encode(make_pos(pos[player])))
    reply = ""
    while True:
        try:
            data = read_pos(conn.recv(2048).decode())
            pos[player] = data
            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = pos[0]
                else:
                    reply = pos[1]

                print("Recieved : ", data)
                print("Sending  : ", reply)

            conn.sendall(str.encode(make_pos(reply)))
        except:
            break

    print("Lost Connection")
    conn.close()


currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to ", addr)
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1



