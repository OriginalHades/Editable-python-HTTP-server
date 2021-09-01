import socket,threading,os,time

defaultHost = os.popen("hostname -I").read().split(" ")[0]

class clientConnection:
    def __init__(self,connection,address,request,server):
        self.connection = connection
        self.address = address
        self.request = request
        self.server = server

        self.autoHeadersEnable = False
        self.toSend = b""

        self.chunkSize = 1024

    def send(self,data):
        if self.autoHeadersEnable:
            self.toSend += bytes(data.encode("utf-8"))
        else:
            self.connection.send(bytes(data.encode("utf-8")))

    def sendRaw(self,data):
        if self.autoHeadersEnable:
            self.toSend += data
        else:
            self.connection.send(data)
    
    def sendFile(self,path):
        if self.autoHeadersEnable:
            self.toSend += open(path,"rb").read()
        else:
            raise Exception("AutoHeaders are not enabled so 'sendFile' is not supported")

    def autoHeaders(self):
        self.toSend = b""
        self.autoHeadersEnable = True
    
    def commit(self,contentType):
        if self.autoHeadersEnable:
            self.connection.send(bytes(
                self.server.generateHeaders(200,
                "OK",
                {
                    "Content-Type":contentType + "; charset=utf-8",
                    "Connection":"Keep-Alive",
                    "Content-length":len(self.toSend)}
                ).encode("utf-8")
            ))
            for a in range(0,len(self.toSend),self.chunkSize):
                self.connection.send(self.toSend[a:a+self.chunkSize])
        else:
            print("Auto headers is not enabled no reason to commit")
        

class Server:
    def __init__(self,host=defaultHost,port=8080):
        self.host = host
        self.port = port

        self.getPathHandlers = {}
        self.postPathHandlers = {}

    def generateHeaders(self,status_code,status,obj):
        out = "HTTP/1.1 " + str(status_code) + " " + str(status) +"\r\n"

        for i,a in enumerate(obj.items()):
            out += str(a[0]) + ": " + str(a[1]) + ("\r\n" if not (i) == len(obj.items())-1 else "")

        out += "\r\n\r\n"

        return out

    def clientHandler(self,connection,address):
        keepAlive = True
        while keepAlive:        
            data = connection.recv(1024)

            if not data:
                break
            else:
                request = self.decodeRequestHeaders(data.decode())
                #headers = self.generateHeaders(200,{"Connection":"Keep-Alive","Content-Type":"text/plain; charset=utf-8"})

                client = clientConnection(connection,address,request,self)
                if request["REQUEST"] == "GET":
                    if request["PATH"] in self.getPathHandlers:
                        self.getPathHandlers[request["PATH"]](client)
                    else:
                        client.send(self.generateHeaders(404,"Not Found",{"Connection":"keep-alive"}))

                if request["REQUEST"] == "POST":
                    if request["PATH"] in self.postPathHandlers:
                        print(request)
                        self.getPathHandlers[request["PATH"]](client,"")
                    else:
                        client.send(self.generateHeaders(404,"Not Found",{"Connection":"keep-alive"}))
                
                if not request["CONNECTION"] == "keep-alive":
                    keepAlive = False

        #connection.send(bytes(body.encode("utf-8")))

    def decodeRequestHeaders(self,headerData):
        out = {}

        headerData = headerData.split("\r\n")
        top = headerData[0].split(" ")
        headerData = headerData[1:]

        out["REQUEST"] = top[0]
        out["PATH"] = top[1]

        for a in headerData:
            b = a.split(": ")
            if len(b) > 1:
                out[b[0].upper()] = b[1]

        return out


    def server_forever(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.bind((self.host, self.port))
            s.listen()
            while True:
                conn, addr = s.accept()
                if conn:
                    print('Connected by', addr)
                    clientHandler = threading.Thread(target=self.clientHandler,args=(conn,addr))
                    clientHandler.start()
        finally:
            s.close()
    
    def get(self,path,callback):
        self.getPathHandlers[path] = callback
    
    def post(self,path,callback):
        self.postPathHandlers[path] = callback