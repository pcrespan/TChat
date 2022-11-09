from socket import *
from ssl import SSLContext
import threading, ssl
import sys

def captureInput():
    ip = input("IP: ")
    port = input("Open port: ")
    return ip, int(port)


# Creating socket with TCP protocol
def getSocket():
    sock = socket(AF_INET, SOCK_STREAM)
    return sock


def getSSLSocket(sock):
    context = SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations("./Test_cert/chat.crt")
    context.load_cert_chain(certfile="./ClientCert/client.crt", keyfile="./ClientCert/client.key")
    SSLSock = context.wrap_socket(sock, server_side=False, server_hostname="127.0.0.1")
    return SSLSock


def connection(ip, port, sock):
    try:
        sock.connect((ip, port))
        print(f"Connected with {ip}")
        return True
    except:
        print("Connection failed")
        return False


def receiveMsg(sock):
    while True:
        msg = sock.recv(1024).decode("utf8")
        print(msg)


def sendMsg(sock):
    msg = bytes(input(""), 'utf8')
    sock.send(msg)


def receiveThread(sock):
    recvThread = threading.Thread(target=receiveMsg, args=(sock, ))
    recvThread.start()
    return recvThread


def getUsername(sock):
    username = ""
    while username == "":
        username = input("Username: ").strip()
    print(f"Welcome to the server, {username}")
    username = bytes(username, "utf8")
    sock.send(username)


def main():
    try:
        ip, port = captureInput()
        sock = getSocket()
        SSLSock = getSSLSocket(sock)
        connection(ip, port, SSLSock)

        # Thread to receive messages
        recvThread = receiveThread(SSLSock)

        # Choose username
        getUsername(sock)
    
        while True:
            sendMsg(SSLSock)
    except:
        recvThread.join()
        SSLSock.close()
        sys.exit(0)


if __name__ == "__main__":
    main()
