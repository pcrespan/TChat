from socket import *
from threading import *
import threading
import sys

def captureInput():
    ip = input("IP: ")
    port = input("Open port: ")
    return ip, int(port)


# Creating socket with TCP protocol
def getSocket():
    sock = socket(AF_INET, SOCK_STREAM)
    return sock


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
        msg = sock.recv(1024)
        stringMsg = str(msg)
        print("\n" + stringMsg)


def sendMsg(sock):
    msg = bytes(input("Message: "), 'utf8')
    sock.send(msg)


def receiveThread(sock):
    recvThread = threading.Thread(target=receiveMsg, args=(sock, ))
    recvThread.start()
    return recvThread


def main():
    try:
        ip, port = captureInput()
        sock = getSocket()
        connection(ip, port, sock)

        # Thread to receive messages
        recvThread = receiveThread(sock)

        while True:
            sendMsg(sock)
    except:
        recvThread.join()
        sock.close()
        sys.exit(0)


if __name__ == "__main__":
    main()