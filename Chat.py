from socket import *
import threading, ssl
import sys


# Function to gather server IP
# port and hostname
def captureInput():
    ip = input("IP: ")
    port = input("Open port: ")
    serverHostname = input("Server hostname: ")
    return ip, int(port), serverHostname


# Creating socket with TCP protocol
def getSocket():
    sock = socket(AF_INET, SOCK_STREAM)
    return sock


# Checks server certificates and returns
# SSL socket
def getSSLSocket(sock, serverHostname):
    # Authenticate server using its certificate
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile="./ServerCert/server.crt")
    # Load client certificates to identify itself to server
    context.load_cert_chain(certfile="./ClientCert/client.crt", keyfile="./ClientCert/client.key")
    # Wraps socket to get a secure connection
    SSLSock = context.wrap_socket(sock, server_side=False, server_hostname=serverHostname)
    return SSLSock


# Attempts to connect to server 
def connection(ip, port, sock):
    try:
        sock.connect((ip, port))
        print(f"Connected with {ip}")
    except Exception as e:
        print("Connection failed: ", e)
        sock.close()


# Receives messages from the server
def receiveMsg(sock):
    while True:
        try:
            msg = sock.recv(1024).decode("utf8")
            print(msg)
        except Exception as e:
            print("An exception has occured: ", e)
            sock.close()
            exit()


# Sends message to the server
def sendMsg(sock):
    msg = bytes(input(""), 'utf8')
    sock.send(msg)


# Thread to run receiveMsg function
def receiveThread(sock):
    recvThread = threading.Thread(target=receiveMsg, args=(sock, ), daemon=True)
    recvThread.start()
    return recvThread


# Gathers username and sends to server
def getUsername(sock):
    username = ""
    while username == "":
        username = input("Username: ").strip()
    print(f"Welcome to the server, {username}")
    username = bytes(username, "utf8")
    sock.send(username)


def main():
    try:
        # Socket/connection
        ip, port, serverHostname = captureInput()
        sock = getSocket()
        SSLSock = getSSLSocket(sock, serverHostname)
        connection(ip, port, SSLSock)

        # Messages and username
        receiveThread(SSLSock)
        getUsername(SSLSock)
    
        while True:
            sendMsg(SSLSock)
    except Exception as e:
        print(e)
        # If an exception occurs, close socket and exit
        sock.close()
        sys.exit(0)


if __name__ == "__main__":
    main()
