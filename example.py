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
    client.commit("text/html")


#Sets the `main` function as the handler for path `/`
server.get("/", main)

#Serve the files in path '.' as '/' on the server
server.static(".", "/")

#Start the server
server.server_forever()
