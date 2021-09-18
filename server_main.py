 
from loading_modules import loading_modules
from server_core import low_interface_of_server

class server:
    def __init__(self):
        
        # loading all neccessary modules which is required to start chatroom server
        self.Modules=loading_modules()
        
        # HOST variable will store the ip address where server will be run
        self.HOST=''

        # asking a port number from user
        while True:
            try:
                print('[CHAT ROOM SERVER NEEDS PORT NUMBER TO RUN]...TYPE IT PLEASE')
                self.PORT = int(input())
                break
            except Exception as e:
                print('Invalid Input')

        # building a socket
        try:
            self.server=self.Modules.socket.socket(self.Modules.socket.AF_INET, self.Modules.socket.SOCK_STREAM)
        except Exception as e:
            self.Modules.logger.error(e)
            print(e)
    
    # start method will start the server
    def start(self):
        self.intialize_server = low_interface_of_server(self.server,self.HOST,self.PORT)

    # stop method is use to pause server
    def stop(self):
        pass

    # exit method will shutdown the server
    def exit(self):
        pass



def core():
    while True:
        print('[ENTER 1 FOR STARTING CHAT-ROOM SERVER AND 0 FOR EXIT]....TYPE IT PLEASE')
        de=input()
        if de=='1':
            room=server()
            room.start()
        elif de=='0':
            break
        else:
            print('Invalid Input')
core()
