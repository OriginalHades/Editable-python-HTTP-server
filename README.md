# Editable WEB Server

This server has inbuild HTTP support for hosting a web page.

`POST request are not yet supported.`

## Starting a server
First we create the server object:  
`Server(host={device local address},port=8080)`
```python
#import the server class
from server import Server

#create class object `server`
server = Server()
```
The arguments of the server are `host` and `port`   
They are defaulted to the devices local address and port `8080`

To handle get request:   
`server.get(path,callback)`

```python
def main(client):
    # Initiates automaticly generated headers based on response content
    client.autoHeaders()

    # Adds `index.html` contents to the response
    client.sendFile("index.html")

    # sends the response with headers
    # note: the content type of response has to be the first argument
    client.commit("text/plain")

#Sets the `main` function as the handler for path `/`
server.get("/",main)
```

To start the server:  
`server.serve_forever()`
```python
#Start the server
server.server_forever()
```

The whole example code:
```python
#import the server class
from server import Server

#create class object `server`
server = Server()

#Main function as a request handler
def main(client):
    # Initiates automaticly generated headers based on response content
    client.autoHeaders()

    # Adds `index.html` contents to the response
    client.sendFile("index.html")

    # sends the response with headers
    # note: the content type of response has to be the first argument
    client.commit("text/plain")

#Sets the `main` function as the handler for path `/`
server.get("/",main)

#Start the server
server.server_forever()
```

## Handler client class

### variables:

- `client.connection` => the connection to the client
- `client.address` => the address of the client
- `client.request` => the HTTP request that was sent by client
- `client.server` => the server instance the client connected to

### Auto headers
If auto generated headers are enabled the data is stored. 

The stored data and headers are sent after calling the function:   
```python
client.commit({content type of response})
```

The auto generated headers can be enabled by calling the function:   
```python
client.autoHeaders()
```

### Send Functions

- `client.send(data)` => sends `string` data converted to `bytes` to the client
- `client.sendRaw(data)` => sends `bytes` data to the client
- `client.sendFile(path)` => sends contents of inputed file to the client

### Send Function with auto headers enabled

- `client.send(data)` => adds `string` data converted to `bytes` to the response
- `client.sendRaw(data)` => adds `bytes` to the response
- `client.sendFile(path)` => adds contents of inputed file to the response