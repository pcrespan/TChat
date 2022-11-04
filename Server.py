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
            threading.Thread(target=self.clientCommunication, args=(con, )).start()
            

    def clientCommunication(self, con):
        while True:
            # Returns empty messages if connection is closed
            msg = con.recv(1024)
            # Testing if message is not empty
            if len(msg) == 0:
                print("Connection closed")
                break
            self.communicateServer(msg)


    # The try except is not allowing for to continue
    def communicateServer(self, msg):
        # Add try except to remove connections
        self.connectedClients = self.clients
        i = 0
        for client in self.clients:
            try:
                client.send(msg)
                print("Sending message...")
                i += 1
            except:
                # Maybe add i+=1 here
                print("A client has disconnected")
                self.connectedClients.pop(i)
                i += 1
                pass
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