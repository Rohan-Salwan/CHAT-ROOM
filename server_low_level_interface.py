from loading_modules import loading_modules

class node:
    def __init__(self,x,z):
        self.sock=x
        self.alt=z

class low_interface_of_server:
    def __init__(self,server,HOST,PORT):
        self.modules=loading_modules()
        # socket bind method will bind the host with port 
        server.bind((HOST,PORT))
        
        # now server is going to listen on this port for connections
        server.listen()
        
        print('CHATROOM SERVER IS ACTIVATED')
        
        # building arrays to store clients and their information
        self.Public_clients=[]
        self.Private_clients=[]
        self.Public_names=[]
        self.Private_names=[]
        
        # kill_thread variable assigned to stop thread execution.  
        self.kill_thread=False
        
        # starting thread of kick method and it will run along with main method 
        t=self.modules.threading.Thread(target=self.kick)
        t.start()
        
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
            ta=self.modules.threading.Thread(target=self.Public_chat_reciever, args=(conn,))
            ta.start()

    def Private_Chat(self):
        v=0
        
        # this loop is going to check private client list that any one is in queue for private chat
        # or not so according to that it will create private chat threads. 
        while True:
            if len(self.Private_clients)<1:
                pass
            elif v == len(self.Private_clients):
                pass
            else:
                # obj variable will collect the client who requested for private chat.
                obj = self.Private_clients[v]
                
                while True:
                    if obj.alt not in self.Public_clients:
                        f1=self.modules.threading.Thread(target=self.Private_chat_Reciever, args=(obj.alt, obj.sock,))
                        f1.start()
                        f2=self.modules.threading.Thread(target=self.Private_chat_Reciever, args=(obj.sock, obj.alt,))
                        f2.start()
                        v+=1
                        break
                    else:
                        pass
    
    # broadcast method will broadcast all messages from client to all other public clients.
    def broadcast(self,message,ex):
        for client in self.Public_clients:
            if client==ex:
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

    # permission method is gonna be in process when private chat mode is requested by client.
    def permission(self,connection):
        connection.sendall('SELECT TNE NAME FROM LIST WHOME TOU WANNA CHAT PRIVATE AND TYPE IT'.encode('ascii'))
        
        # In this loop server connected client list is going to send that client who requested for private chat.
        for name in self.Public_names:
            connection.sendall(name.encode('ascii'))
        
        # retrieve a name from client whom it want to do privatechat with. 
        dataa=connection.recv(1024)
        dataa=dataa.decode()
        
        # response will be in specific format so here it is gonna split.
        dataa=dataa.split(':  ')
        recievername=dataa[1]
        sendername=dataa[0]
        
        # retrieving sockets and index from arrays to establish the communication between private chat participants.
        a=self.Public_names.index(recievername)
        recieversocket=self.Public_clients[a]
        msgg=sendername+'USER REQUEST YOU FOR PRIVATECHAT ENTER /YES TO JOIN PRIVATECHAT'
        recieversocket.sendall(msgg.encode('ascii'))
        
        # filling private chat clients sockets and names to arrays
        self.Private_names.append(sendername)
        connectio=node(connection,recieversocket)
        self.Private_clients.append(connectio)
        self.Public_clients.remove(connection)
        self.Public_names.remove(sendername)

    # Public_chat_reciever method use to recieve messages from public chat users and deliever it to other users.
    def Public_chat_reciever(self,connection):
        while True:
            try:
                if kill_thread==True:
                    kill_thread=False
                    break
            except:
                try:
                    data=connection.recv(1024)
                    if data.decode()=='/PRIVATECHAT':
                        self.permission(connection)
                        kill_thread=True
                    elif data.decode()=='/YES':
                        k=self.Public_clients.index(connection)
                        name=self.Public_names[k]
                        self.Public_clients.remove(connection)
                        self.Public_names.remove(name)
                        kill_thread=True
                    else:
                        try:
                            x=self.Public_clients.index(connection)
                            self.broadcast(data,connection)
                        except:
                            connection.close()
                            break
                except:
                    connection.close()
                    break
    
    # kick method is a feature for server side admin so if admin want to kick any user so it will be able with
    # the help of kick method which will be constantly in working because of thread framework.   
    def kick(self):
        
        # This loop will enlist all public chat users on server side which are actively connected to server.
        while True:
            decison=input('If you want to display user list press 0 and if you want to kick user press 1')
            if decison=='0':
                for name in self.Public_names:
                    print(name)
            elif decison=='1':
                # If someone press 1 then it will enlist the public chat users list
                print('USERS LIST')
                for name in self.Public_names:
                    print(name)
                
                # it will also ask about name from admin whome admin want to kick out.
                n=input('Wanna kick user ENTER THE NAME PLZ')
                index=self.Public_names.index(n)
                
                # retrieving socket from array with th help of index
                con=self.Public_clients[index]
                
                # broadcasting kicked message to all connected public chat users
                msg='USER '+n+' IS KICKED BY CHAT ROOM ADMIN'
                self.broadcast(msg.encode('ascii'),con)
                
                # removing traces of kicked client from server side database.
                self.Public_names.remove(n)
                self.Public_clients.remove(con)
                msg='KICKED'
                con.sendall(msg.encode('ascii'))