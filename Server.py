from socket import *
import threading, ssl
from Chat import getSocket
import pprint

class Server:
    def __init__(self):
        # Initializing server
        self.clients = []
        self.connectedClients = []
        self.sock = getSocket()


    # Returns socket that wraps connection
    def getSSLSocket(self, con):
        # Authenticate client, requiring certificate
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH, cafile="./ClientCert/client.crt")
        context.verify_mode = ssl.CERT_REQUIRED
        # Server certificate identity
        context.load_cert_chain(certfile="./Test_cert/chat.crt", keyfile="./Test_cert/chat.key")
        SSLSock = context.wrap_socket(con, server_side=True)
        # Printing client certificate
        pprint.pprint(SSLSock.getpeercert())
        return SSLSock


    # Binding socket to server
    def bindSocket(self, serverIP, port):
        self.sock.bind((serverIP, port))


    # Listening for connections
    def socketListen(self, n):
        self.sock.listen(n)

    
    # Accepting connections
    def acceptConnection(self):
        while True:
            con, senderIP = self.sock.accept()
            # Attempting to wrap connection with SSL socket
            try:
                SSLSock = self.getSSLSocket(con)
            # If exception occurs, close socket and continue listening
            except Exception as e:
                print("Connection refused: ", e)
                con.close()
                continue
            print(f"{senderIP} connected to the server")
            # Adding connection to clients list
            self.clients.append(SSLSock)
            # Initializing thread to receive and communicate messages
            # to all clients
            threading.Thread(target=self.clientCommunication, args=(SSLSock, ), daemon=True).start()
           
    
    def alertJoin(self, user):
        self.communicateServer(f"{user} has joined the server".encode("utf8"))


    def alertDisconnect(self, user):
        self.communicateServer(f"{user} has disconnected from the server".encode("utf8"))

    
    # Broadcasting messages to all clients
    def clientCommunication(self, con):
        # Gathering username
        user = con.recv(1024).decode("utf8")
        formattedUser = (user + ": ").encode("utf8")
        self.alertJoin(user)

        while True:
            # Returns empty messages if connection is closed
            msg = con.recv(1024)
            # Testing if message is not empty
            if len(msg) == 0:
                print("Connection closed")
                self.alertDisconnect(user)
                break
            # Broadcasting message
            self.communicateServer(formattedUser + msg)


    # Broadcast messages
    def communicateServer(self, msg):
        self.connectedClients = self.clients.copy()
        # Attempts to send message to all clients
        for index, client in enumerate(self.clients):
            try:
                client.send(msg)
                print("Sending message...")
            except:
                # If exception occurs, remove client from copy of clients list
                print("A client has disconnected")
                self.connectedClients.pop(index)
                # Continue loop to send messages
                continue
        # Update clients list
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
