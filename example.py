from server import Server

server = Server()
print(server.host + ":" + str(server.port))

def main(client):
    client.autoHeaders()

    client.sendFile("headers.txt")

    client.commit("text/plain")

def hello(client):
    client.autoHeaders()

    client.send("Hello")

    client.commit("text/plain")

server.get("/",main)

server.get("/hello",hello)

server.server_forever()