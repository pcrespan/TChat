from socket import *
from Chat import getSocket, sendMsg, receiveMsg, sendThread, receiveThread


def bindSocket(sock, serverIP, port):
    sock.bind((serverIP, port))


def socketListen(sock, n):
    sock.listen(n)


def acceptConnection(sock):
    con, senderIP = sock.accept()
    print(f"Connected to {senderIP}")
    return con, senderIP


def main():
    serverIP = "127.0.0.1"
    port = int(input("Port to listen for connections: "))

    sock = getSocket()
    bindSocket(sock, serverIP, port)
    socketListen(sock, 1)

    while True:
        con, senderIP = acceptConnection(sock)
        try:
            while True:
                sendThread(con)
                receiveMsg(con)
        except:
            print("Connection closed")
            break


if __name__ == "__main__":
    main()