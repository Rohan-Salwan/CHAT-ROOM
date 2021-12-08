from loading_modules import loading_modules
class client:
    def __init__(self):
        
        self.passing_key_words = {'/PRIVATECHAT': "", '/YES': ""}

        self.breaking_keywords = {'KICKED': ""}

        self.connection_closed = False

        # loading all neccessary modules which is required to start client
        modules=loading_modules()
        
        HOST = ''
        # Asking user to enter port number please
        while True:
            try:
                print('[YOU NEED TO ENTER THE PORT NUMBER TO CONNECT WITH CHAT ROOM SERVER]....TYPE IT PLEASE')
                PORT = int(input())
                break
            except:
                print('INVALID INPUT')
        
        # asking full name from user
        self.name=input('ENTER YOUR NAME PLZ')
        
        # building a client socket
        sock=modules.socket.socket(modules.socket.AF_INET, modules.socket.SOCK_STREAM)

        # trying to connect client socket with server
        try:
            sock.connect((HOST, PORT))
        except:
            print('NOT ABLE TO CONNECT WITH SERVER[Connection Failed]')

        print('[CONNECTED TO CHAT-ROOM SERVER]........')
        
        # creating reciever and sender threads for client
        Client_reciever_thread=modules.threading.Thread(target=self.reciever, args=(sock,))
        Client_reciever_thread.start()
        Client_sender_thread=modules.threading.Thread(target=self.sender, args=(sock,))
        Client_sender_thread.start()

    # reciever method use for recieving messages form chat room server and run along with sender method with the help of threading framework.
    def reciever(self,connection):
        while True:    
            try:
                data=connection.recv(1024)
                if data.decode() in self.breaking_keywords:
                    self.connection_closed = True
                    break
                else:
                    print(data.decode())
            except:
                connection.close()
                break

    # sender method use for sending messages to chat room server and run along with reciever method with the help of threading framework.
    def sender(self,connectionn):
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

User_client = client()
