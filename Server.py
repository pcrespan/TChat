from socket import *
from threading import *
import threading
from Chat import getSocket


global clients
clients = {}

def bindSocket(sock, serverIP, port):
    sock.bind((serverIP, port))


def socketListen(sock, n):
    sock.listen(n)


def acceptConnection(sock):
    while True:
        con, senderIP = sock.accept()
        print(f"{senderIP} connected to the server")
        clients[con] = senderIP
        threading.Thread(target=clientCommunication, args=(con, ), daemon=True).start()
        


def clientCommunication(con):
    while True:
        msg = con.recv(1024)
        communicateServer(msg)


def communicateServer(msg):
    for client in clients:
        client.send(msg)


def main():
    serverIP = "127.0.0.1"
    port = int(input("Port to listen for connections: "))

    sock = getSocket()
    bindSocket(sock, serverIP, port)
    socketListen(sock, 2)
    acceptConnection(sock)

    
if __name__ == "__main__":
    main()