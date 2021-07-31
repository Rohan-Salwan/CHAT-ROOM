import threading
import socket

HOST = ''
PORT = 1231
name=input('ENTER YOUR NAME PLZ')
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print('connected to server')
def reciever(connection):
    while True:    
        try:
            data=connection.recv(1024)
            data=data.decode()
            if data=='KICKED':
                break
            else:
                print(data)
        except:
            connection.close()
            break
def sender(connectionn):
    i=0
    while True:
        if i==0:
            message=name
            i+=1
        else:
            message=input('')
            message=name+':  '+message
        connectionn.sendall(message.encode('ascii'))
reciever_thread=threading.Thread(target=reciever, args=(s,))
reciever_thread.start()
sender_thread=threading.Thread(target=sender, args=(s,))
sender_thread.start()
