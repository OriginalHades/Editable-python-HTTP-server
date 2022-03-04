#import the server class
from server import Server

#create class object `server`
server = Server()

#print the host and port
print(server.host, server.port)

#Main function as a request handler
def main(client):
    # Initiates automaticly generated headers based on response content
    client.autoHeaders()

    # Adds `index.html` contents to the response
    client.sendFile("index.html")

    # sends the response with headers
    client.commit("text/html")

#Main post as a request handler
def main_post(client,data):
    #Prints post raw request body
    print(data)

    # Initiates automaticly generated headers based on response content
    client.autoHeaders()

    # Adds `index.html` contents to the response
    client.sendFile("index.html")

    # sends the response with headers
    client.commit("text/html")

#Sets the `main` function as the get handler for path `/`
server.get("/", main)
#Sets the `main_post` function as the post handler for path `/`
server.post("/", main_post)

#Serve the files in path './public' as '/' on the server
server.static("./public", "/")

#Start the server
server.server_forever()