from socket import *
from threading import *
import threading
from Chat import getSocket


global clients
clients = {}
global connectedClients
global threads
threads = {}
connectedClients = clients

def bindSocket(sock, serverIP, port):
    sock.bind((serverIP, port))


def socketListen(sock, n):
    sock.listen(n)


def acceptConnection(sock):
    while True:
        con, senderIP = sock.accept()
        print(f"{senderIP} connected to the server")
        clients[con] = senderIP
        threads[con] = threading.Thread(target=clientCommunication, args=(con, ))
        threads[con].start()
    

def clientCommunication(con):
    while True:
        msg = con.recv(1024)
        print("recebi")
        communicateServer(msg)


def communicateServer(msg):
    # Add try except to remove connections
    global clients
    global connectedClients
    connectedClients = clients
    for client in clients:
        try:
            client.send(msg)
        except:
            print(f"{clients[client]} has disconnected")
            connectedClients.pop(client)
    clients = connectedClients


def main():
    serverIP = "127.0.0.1"
    port = int(input("Port to listen for connections: "))

    sock = getSocket()
    bindSocket(sock, serverIP, port)
    socketListen(sock, 1)
    acceptConnection(sock)

    
if __name__ == "__main__":
    main()