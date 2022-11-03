from socket import *
from threading import *
import threading
from Chat import getSocket


class Server:
    def __init__(self):
        self.clients = []
        self.connectedClients = []
        self.sock = getSocket()

    def bindSocket(self, serverIP, port):
        self.sock.bind((serverIP, port))


    def socketListen(self, n):
        self.sock.listen(n)


    def acceptConnection(self):
        while True:
            con, senderIP = self.sock.accept()
            print(f"{senderIP} connected to the server")
            self.clients.append(con)
            print(self.clients)
            threading.Thread(target=self.clientCommunication, args=(con, )).start()
            

    def clientCommunication(self, con):
        while True:
            msg = con.recv(1024)
            if len(msg) == 0:
                print("Conexao fechou")
                break
            self.communicateServer(msg)


    def communicateServer(self, msg):
        # Add try except to remove connections
        self.connectedClients = self.clients
        i = 0
        for client in self.clients:
            try:
                client.send(msg)
                print("enviando")
                i += 1
            except:
                print("A client has disconnected")
                self.connectedClients.pop(i)
        self.clients = self.connectedClients


def main():
    serverIP = "127.0.0.1"
    port = int(input("Port to listen for connections: "))
    server = Server()
    sock = getSocket()
    server.bindSocket(serverIP, port)
    server.socketListen(1)
    server.acceptConnection()

    
if __name__ == "__main__":
    main()