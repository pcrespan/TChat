from socket import *

serverIP = "127.0.0.1"
port = int(input("Port to listen for connections: "))

sock = socket(AF_INET, SOCK_STREAM)
sock.bind((serverIP, port))
listener = sock.listen(1)

while True:
    con, senderIP = sock.accept()
    print(f"Connected to {senderIP}")
    con.send(b"Hello there")
    while True:
        msg = con.recv(1024)
        if not msg:
            break
        print(str(msg))
        sendMsg = bytes(input("Message: "), 'utf-8')
        if sendMsg:
            bMsg = bytes(sendMsg)
            con.send(bMsg)