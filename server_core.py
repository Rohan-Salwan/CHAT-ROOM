from loading_modules import loading_modules

class node:
    def __init__(self,Sender,Receiver):
        self.sock = Sender
        self.alt = Receiver

class low_interface_of_server:
    def __init__(self,server,HOST,PORT):
        self.modules=loading_modules()
        # socket bind method will bind the host with port 
        server.bind((HOST,PORT))
        
        # now server is going to listen on this port for connections
        server.listen()
        
        print('CHATROOM SERVER IS ACTIVATED')
        
        # building arrays to store clients and their information
        self.Public_names, self.Private_names, self.Private_clients, self.Public_clients = [], [], [], []
        
        # kill_thread variable assigned to stop thread execution.  
        self.kill_thread=False
        
        # starting thread of kick method and it will run along with main method 
        Kick_thread=self.modules.threading.Thread(target=self.kick)
        Kick_thread.start()
        
        # main method execution will start the server
        self.Main(server)

    def Main(self,server):
        
        # Private chat thread is going to execute along with public chat thread
        Private_Chat_Thread=self.modules.threading.Thread(target=self.Private_Chat)
        Private_Chat_Thread.start()
        
        while True:
            conn, addr=server.accept()
            # conn is a socket which is connected to server now
            
            print('CONNECTED TO', addr)
            
            # filling client socket in public client array
            self.Public_clients.append(conn)
            
            conn.sendall('YOU HAVE JOINDED THE CHATROOM'.encode('ascii'))
            
            # server is recieving names from clients
            name=conn.recv(1024)
            
            self.Public_names.append(name.decode())
            
            # Public chat thread is going to excecute
            Public_Chat_Thread = self.modules.threading.Thread(target=self.Public_chat_reciever, args=(conn,))
            Public_Chat_Thread.start()

    def Private_Chat(self):
        v = 0
        
        # this loop is going to check private client list that any one is in queue for private chat
        # or not so according to that it will create private chat threads. 
        while True:
            if len(self.Private_clients)<1 or v == len(self.Private_clients):
                pass
            else:
                # obj variable will collect the client who requested for private chat.
                obj = self.Private_clients[v]
                
                while True:
                    if obj.alt not in self.Public_clients:
                        private_thread = self.modules.threading.Thread(target=self.Private_chat_Reciever, args=(obj.alt, obj.sock,))
                        private_thread.start()
                        private_alt_thread=self.modules.threading.Thread(target=self.Private_chat_Reciever, args=(obj.sock, obj.alt,))
                        private_alt_thread.start()
                        v+=1
                        break
    
    # broadcast method will broadcast all messages from client to all other public clients.
    def broadcast(self,message,ex):
        for client in self.Public_clients:
            if client == ex:
                pass
            else:
                client.sendall(message)
    
    # Private_chat_reciever method will be use in private chat threads. 
    def Private_chat_Reciever(self,sender,reciever):
        while True:
            try:
                dataaa=sender.recv(1024)
                reciever.sendall(dataaa)
            except:
                sender.close()
                break

    def Enlist_Public_Users(self, Public_names, exuser=None, connection=None):
        for name in Public_names:
            if exuser == name:
                exuser = None
            elif connection:
                connection.sendall(name.encode('ascii'))
            else:
                print(name)

    # PrivateChat_Permission method is gonna be in process when private chat mode is requested by client.
    def PrivateChat_Permission(self,connection):
        connection.sendall('SELECT TNE NAME FROM LIST WHOME TOU WANNA CHAT PRIVATE AND TYPE IT'.encode('ascii'))
        
        Index = self.Public_clients.index(connection)
        name = self.Public_names[Index]

        # Enlist_Public_Users method with connection parameter will forward the connected clients list  to user who requested for private chat.
        self.Enlist_Public_Users(self.Public_names, exuser=name, connection=connection)
        
        # retrieve a name from client whom it want to do privatechat with. 
        dataa = connection.recv(1024)
        dataa = dataa.decode()
        
        # response will be in specific format so here it is gonna split.
        dataa = dataa.split(':  ')
        recievername = dataa[1]
        sendername = dataa[0]
        
        # retrieving sockets and index from arrays to establish the communication between private chat participants.
        index=self.Public_names.index(recievername)
        recieversocket = self.Public_clients[index]
        msgg=sendername+'USER REQUEST YOU FOR PRIVATECHAT ENTER /YES TO JOIN PRIVATECHAT'
        recieversocket.sendall(msgg.encode('ascii'))
        
        # filling private chat clients sockets and names to arrays
        self.Private_names.append(sendername)
        connection = node(connection,recieversocket)
        self.Private_clients.append(connection)
        self.Public_clients.remove(connection)
        self.Public_names.remove(sendername)

    # Public_chat_reciever method use to recieve messages from public chat users and deliever it to other users.
    def Public_chat_reciever(self,connection):
        while True:
            data=connection.recv(1024)
            if data.decode() == '/PRIVATECHAT':
                self.PrivateChat_Permission(connection)
                break
            elif data.decode() == '/YES':
                index = self.Public_clients.index(connection)
                name = self.Public_names[index]
                self.Public_clients.remove(connection)
                self.Public_names.remove(name)
                break
            elif data.decode() == '/EXIT':
                index = self.Public_clients.index(connection)
                del_name=self.Public_names[index]
                self.Public_names.remove(del_name)
                self.Public_clients.remove(connection)
                connection.close()
                break
            else:
                self.broadcast(data,connection)
    
    # kick method is a feature for server side admin so if admin want to kick any user so it can kick with
    # the help of kick method which will be constantly in working because of thread framework.   
    def kick(self):
        while True:
            decison=input('If you want to display user list press 0 and if you want to kick user press 1')

            # if decison is '0' then it will display connected users list.
            if decison == '0':
                self.Enlist_Public_Users(self.Public_names)
            elif decison == '1':
                # If someone press 1 then it will enlist the public chat users list specifically for removing task.
                print('USERS LIST')
                self.Enlist_Public_Users(self.Public_names)
                
                # it will also ask about name from admin whome admin want to kick out.
                Dumping_Name = input('Wanna kick user ENTER THE NAME PLZ')
                index=self.Public_names.index(Dumping_Name)
                
                # retrieving socket from array with th help of index
                con=self.Public_clients[index]
                con.sendall('KICKED'.encode('ascii'))

                # broadcasting kicked message to all connected public chat users
                msg='USER '+Dumping_Name+' IS KICKED BY CHAT ROOM ADMIN'
                self.broadcast(msg.encode('ascii'),con)