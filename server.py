import threading
import socket

HOST=''
PORT=1417
server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST,PORT))
server.listen()
print('CHATROOM SERVER IS ACTIVATED')
Public_clients=[]
Private_clients=[]
Public_names=[]
Private_names=[]
kill_thread=False
class node:
    def __init__(self,x,z):
        self.sock=x
        self.alt=z

def Main(server,Public_clients,Private_clients):
    Private_Chat_Thread=threading.Thread(target=Private_Chat, args=(Private_clients,))
    Private_Chat_Thread.start()
    while True:
        conn, addr=server.accept()
        print('CONNECTED TO', addr)
        Public_clients.append(conn)
        conn.sendall('YOU HAVE JOINDED THE CHATROOM'.encode('ascii'))
        name=conn.recv(1024)
        Public_names.append(name.decode())
        ta=threading.Thread(target=reciever, args=(conn,))
        ta.start()

def Private_Chat(Private_clients):
    v=0
    while True:
        if len(Private_clients)<1:
            pass
        elif v == len(Private_clients):
            pass
        else:
            obj = Private_clients[v]
            while True:
                if obj.alt not in Public_clients:
                    f1=threading.Thread(target=AR, args=(obj.alt, obj.sock,))
                    f1.start()
                    f2=threading.Thread(target=AR, args=(obj.sock, obj.alt,))
                    f2.start()
                    v+=1
                    break
                else:
                    pass

def broadcast(message,ex):
    for client in Public_clients:
        if client==ex:
            pass
        else:
            client.sendall(message)

def AR(sender,reciever):
    while True:
        try:
            dataaa=sender.recv(1024)
            reciever.sendall(dataaa)
        except:
            sender.close()
            break

def permission(connection):
    connection.sendall('SELECT TNE NAME FROM LIST WHOME TOU WANNA CHAT PRIVATE AND TYPE IT'.encode('ascii'))
    for name in Public_names:
        connection.sendall(name.encode('ascii'))
    dataa=connection.recv(1024)
    dataa=dataa.decode()
    dataa=dataa.split(':  ')
    recievername=dataa[1]
    sendername=dataa[0]
    a=Public_names.index(recievername)
    recieversocket=Public_clients[a]
    msgg=sendername+'USER REQUEST YOU FOR PRIVATECHAT ENTER /YES TO JOIN PRIVATECHAT'
    recieversocket.sendall(msgg.encode('ascii'))
    Private_names.append(sendername)
    connectio=node(connection,recieversocket)
    Private_clients.append(connectio)
    Public_clients.remove(connection)
    Public_names.remove(sendername)

def reciever(connection):
    while True:
        try:
            if kill_thread==True:
                kill_thread=False
                break
        except:
            try:
                data=connection.recv(1024)
                if data.decode()=='/PRIVATECHAT':
                    permission(connection)
                    kill_thread=True
                elif data.decode()=='/YES':
                    k=Public_clients.index(connection)
                    name=Public_names[k]
                    Public_clients.remove(connection)
                    Public_names.remove(name)
                    kill_thread=True
                else:
                    try:
                        x=Public_clients.index(connection)
                        broadcast(data,connection)
                    except:
                        connection.close()
                        break
            except:
                connection.close()
                break
def kick():
    while True:
        decison=input('If you want to display user list press 0 and if you want to kick user press 1')
        if decison=='0':
            for name in Public_names:
                print(name)
        elif decison=='1':
            print('USERS LIST')
            for name in Public_names:
                print(name)
            n=input('Wanna kick user ENTER THE NAME PLZ')
            index=Public_names.index(n)
            con=Public_clients[index]
            msg='USER '+n+' IS KICKED BY CHAT ROOM ADMIN'
            broadcast(msg.encode('ascii'),con)
            Public_names.remove(n)
            Public_clients.remove(con)
            msg='KICKED'
            con.sendall(msg.encode('ascii'))

t=threading.Thread(target=kick)
t.start()
Main(server,Public_clients,Private_clients)