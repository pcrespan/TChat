from socket import *
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
        user = con.recv(1024).decode("utf8")
        formattedUser = (user + ": ").encode("utf8")

        while True:
            # Returns empty messages if connection is closed
            msg = con.recv(1024)
            # Testing if message is not empty
            if len(msg) == 0:
                print("Connection closed")
                break
            self.communicateServer(formattedUser + msg)


    def communicateServer(self, msg):
        # Add try except to remove connections
        self.connectedClients = self.clients.copy()
        for index, client in enumerate(self.clients):
            try:
                client.send(msg)
                print("Sending message...")
            except:
                print("A client has disconnected")
                self.connectedClients.pop(index)
                continue 
        self.clients = self.connectedClients


def main():
    serverIP = "127.0.0.1"
    port = int(input("Port to listen for connections: "))
    server = Server()
    server.bindSocket(serverIP, port)
    server.socketListen(2)
    server.acceptConnection()

    
if __name__ == "__main__":
    main()
