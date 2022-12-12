# TChat

## Description

TChat is a local network chat app based on terminals written in Python. It uses Python's `ssl` library, which allows for mutual authentication between the server and client, using CA certificates to create a secure connection. It also uses `threads` to run parts of the code, allowing real time message exchanging.

## Server.py

`Server.py` is the file containing the server-side of the chat. It must be opened before `Chat.py`. The user will be asked for a port number to listen for connections. After an attempt of connection, the server will either accept it if the client is known by the server, or refuse it on every other case.

> 1. User is prompted for port number to listen for connections
> 2. TCP protocol socket is created
> 3. Socket is bound to server
> 4. Socket waits for connection
> 5. Connection is made
> 6. Attempts to wrap connection socket with SSL
> 7. If client uses invalid certificates, connection is refused and closed
> 8. Otherwise, connection is accepted
> 7. Client is added to clients list
> 8. Thread is created to receive messages from client
> 9. After receiving client message, broadcast to all clients using `clientCommunication`
> 10. If an exception occurs during `clientCommunication`, delete client that caused error from clients list and close connection

## Chat.py

`Chat.py` is the file containing the client-side of the chat. It will ask the user for the `server IP address`, `port number` and `server hostname` - which is represented by the `common name (CN)` field on the server certificate. After that, the user will be prompted for a username to be used on the server.

> 1. TCP protocol sockets are created
> 2. The sockets are wrapped by `context.wrap_socket()`, which is created using Python's default configurations
> 3. The sockets now use certificates to communicate with each other
> 4. The connection is made using the wrapped socket
> 5. Server checks for client certificate
> 6. If client uses valid certificate, connection is accepted

## Creating certificates
CA certificates must be created for the server and client, using `openssl`:

### Server-side

Inside of the cloned repository, create directory `ServerCert` with

```
mkdir ServerCert
```

Change directory to `ServerCert`:
```
cd ServerCert
```

Create server certificate:

#### ATTENTION:
> - You will be prompted for information to create the certificates
> - The `server hostname` used by the client to connect to the server will be the `common name (CN)` that the user provided for the server certificate

```
openssl req -newkey rsa:4096 -x509 -sha256 -days 365 -nodes -out server.crt -keyout server.key
```

### Client-side

Create directory ClientCert:

```
mkdir ClientCert
```

Change directory:

```
cd ClientCert
```

Create client certificate:

```
openssl req -newkey rsa:4096 -x509 -sha256 -days 365 -nodes -out client.crt -keyout client.key
```

## Usage

#### Server-side:

Open the server locally on terminal:

```
python Server.py
```

Select the port that will listen for connections.

#### Client-side

Open client on another terminal (using the client computer):

```
python Chat.py
```

For the server IP, use its private IP address - which can be found by using `ifconfig` (on Linux/Mac) or `ipconfig` (on Windows) on another terminal in the server. Then, you select the same port opened by the server. Finally, provide the server hostname - which is located on "Common name" on the server certificate (server.crt)

## Requirements

> python 3.10.x
> openssh
