from socket import *
import threading, ssl
from Chat import getSocket
import pprint

class Server:
    def __init__(self):
        self.clients = []
        self.connectedClients = []
        self.sock = getSocket()


    def getSSLSocket(self, con):
        # Authenticate client
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH, cafile="./ClientCert/client.crt")
        context.verify_mode = ssl.CERT_REQUIRED
        # Server certificate identity
        context.load_cert_chain(certfile="./Test_cert/chat.crt", keyfile="./Test_cert/chat.key")
        SSLSock = context.wrap_socket(con, server_side=True)
        pprint.pprint(SSLSock.getpeercert())
        return SSLSock


    def bindSocket(self, serverIP, port):
        self.sock.bind((serverIP, port))


    def socketListen(self, n):
        self.sock.listen(n)


    def acceptConnection(self):
        while True:
            con, senderIP = self.sock.accept()
            try:
                SSLSock = self.getSSLSocket(con)
            except Exception as e:
                print("Connection refused: ", e)
                con.close()
                continue
            print(f"{senderIP} connected to the server")
            self.clients.append(SSLSock)
            threading.Thread(target=self.clientCommunication, args=(SSLSock, )).start()
           

    def alertJoin(self, user):
        self.communicateServer(f"{user} has joined the server".encode("utf8"))


    def alertDisconnect(self, user):
        self.communicateServer(f"{user} has disconnected from the server".encode("utf8"))


    def clientCommunication(self, con):
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
