from socket import *
from threading import *
import threading

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
    receiveThread = threading.Thread(target=receiveMsg, args=(sock, ), daemon=True)
    receiveThread.start()


def main():
    ip, port = captureInput()
    sock = getSocket()
    connection(ip, port, sock)

    # Thread to receive messages
    receiveThread(sock)

    while True:
        sendMsg(sock)


if __name__ == "__main__":
    main()