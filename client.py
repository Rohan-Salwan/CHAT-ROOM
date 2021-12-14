from loading_modules import loading_modules
class Client:
    def __init__(self, test_port = None, test_name = None):
        
        self.passing_key_words = {'/PRIVATECHAT': "", '/YES': ""}

        self.breaking_keywords = {'KICKED': ""}

        self.connection_closed = False

        # loading all neccessary modules which is required to start client
        modules=loading_modules()
        
        self.HOST = ''

        # Asking user to enter port number please
        print('[YOU NEED TO ENTER THE PORT NUMBER TO CONNECT WITH CHAT ROOM SERVER]....TYPE IT PLEASE')
        if not test_port:
            self.PORT = self.Obtaining_UserInput(Type=int)
        else:
            self.PORT = test_port
        
        # asking full name from user
        print('ENTER YOUR NAME PLZ')
        if not test_name:
            self.name = self.Obtaining_UserInput(Type=str)
        else:
            self.name = test_name
        
        # building a client socket
        self.sock = modules.socket.socket(modules.socket.AF_INET, modules.socket.SOCK_STREAM)

        # trying to connect client socket with server
        try:
            self.sock.connect((self.HOST, self.PORT))
        except:
            print('NOT ABLE TO CONNECT WITH SERVER[Connection Failed]')

        print('[CONNECTED TO CHAT-ROOM SERVER]........')
        # creating reciever and sender threads for client
        if not test_port:
            Client_reciever_thread = modules.threading.Thread(target=self.reciever, args=(self.sock,))
            Client_reciever_thread.start()
            Client_sender_thread = modules.threading.Thread(target=self.sender, args=(self.sock,))
            Client_sender_thread.start()

    # Obtaing_UserInput method get information from user according to its Type parameter.
    def Obtaining_UserInput(self, Type=None):
        while True:
            try:
                User_Info = Type(input())
                return User_Info
            except:
                print('INVALID INPUT')

    # reciever method use for recieving messages form chat room server and run along with sender method with the help of threading framework.
    def reciever(self, connection):
        while True:    
            try:
                self.data = connection.recv(1024)
                if self.data.decode() in self.breaking_keywords:
                    self.connection_closed = True
                    break
                else:
                    print(self.data.decode())
            except:
                connection.close()
                break

    # sender method use for sending messages to chat room server and run along with reciever method with the help of threading framework.
    def sender(self, connectionn):
        connectionn.sendall(self.name.encode('ascii'))
        while True:
            message = input('')
            if message == '/EXIT' or self.connection_closed:
                connectionn.sendall('/EXIT'.encode('ascii'))
                connectionn.close()
                break
            else:
                if message not in self.passing_key_words:
                    message = self.name+':  '+message
                connectionn.sendall(message.encode('ascii'))
