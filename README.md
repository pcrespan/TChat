# RealtimeChat

## Description

RealtimeChat is a chat app based on terminals written in Python. A server must be opened for the clients to connect. It uses Python's `ssl` library, which allows for mutual authentication between the server and client, using CA certificates to create a secure connection. It also uses `threads` to run parts of the code, allowing real time message exchanging.

## Server.py

`Server.py` is the file containing the server-side of the chat. It must be opened before `Chat.py`. The user will be asked for a port number to listen for connections. After an attempt of connection, the server will either accept it if the client is known by the server, or refuse it on every other case.

## Chat.py

`Chat.py` is the file containing the client-side of the chat. It will ask the user for the `server IP address`, `port number` and `server hostname` - which is represented by the `common name (CN)` field on the server certificate. After that, the user will be prompted for a username to be used on the server.

> ### How does it work?
>
> 1. TCP protocol sockets are created
> 2. The sockets are wrapped by `context.wrap_socket()`, which is created using Python's default configurations
> 3. The sockets now use certificates to communicate with each other
> 4. The connection is made using the wrapped socket
> 5. Server checks for client certificate
> 6. If client uses valid certificate, accept connection
> 7. Client is added to clients list
> 8. Thread is created on server-side to receive messages from client
> 9. After receiving client message, broadcast to all clients using `clientCommunication`
> 10. If an exception occurs during `clientCommunication`, delete client that caused error from clients list and close connection

## Usage
CA certificates must be created for the server and client, using `openssl`:

### Server-side

```
openssl req -newkey rsa:4096 -x509 -sha256 -days 365 -nodes -out server.crt -keyout server.key
```

### Client-side

```
openssl req -newkey rsa:4096 -x509 -sha256 -days 365 -nodes -out client.crt -keyout client.key
```
