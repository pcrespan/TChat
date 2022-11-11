from socket import *
import threading, ssl
import sys

def captureInput():
    ip = input("IP: ")
    port = input("Open port: ")
    serverHostname = input("Server hostname: ")
    return ip, int(port), serverHostname


# Creating socket with TCP protocol
def getSocket():
    sock = socket(AF_INET, SOCK_STREAM)
    return sock


def getSSLSocket(sock, serverHostname):
    # Authenticate server using its certificate
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile="./Test_cert/chat.crt")
    # Load self certificates to identify itself to server
    context.load_cert_chain(certfile="./ClientCert/client.crt", keyfile="./ClientCert/client.key")
    SSLSock = context.wrap_socket(sock, server_side=False, server_hostname=serverHostname)
    return SSLSock


def connection(ip, port, sock):
    try:
        sock.connect((ip, port))
        print(f"Connected with {ip}")
        return True
    except:
        print("Connection failed")
        sock.close()
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
        ip, port, serverHostname = captureInput()
        sock = getSocket()
        SSLSock = getSSLSocket(sock, serverHostname)
        connection(ip, port, SSLSock)

        # Thread to receive messages
        recvThread = receiveThread(SSLSock)

        # Choose username
        getUsername(SSLSock)
    
        while True:
            sendMsg(SSLSock)
    except:
        recvThread.join()
        SSLSock.close()
        sys.exit(0)


if __name__ == "__main__":
    main()
