import threading
import socket

HOST=''
PORT=1275
server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST,PORT))
server.listen()
print('CHATROOM SERVER IS ACTIVATED')
clients=[]
names=[]
kill_thread=False
recieversocket=None
def listner(server):
    while True:
        conn, addr=server.accept()
        print('CONNECTED TO', addr)
        clients.append(conn)
        conn.sendall('YOU HAVE JOINDED THE CHATROOM'.encode('ascii'))
        name=conn.recv(1024)
        names.append(name.decode())
        ta=threading.Thread(target=reciever, args=(conn,))
        ta.start()

def broadcast(message,ex):
    for client in clients:
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

def reciever(connection):
    while True:
        try:
            if kill_thread==True and recieversocket!=None:
                kill_thread=False
                break
        except:
            try:
                data=connection.recv(1024)
                if data.decode()=='/PRIVATECHAT':
                    connection.sendall('SELECT TNE NAME FROM LIST WHOME TOU WANNA CHAT PRIVATE AND TYPE IT'.encode('ascii'))
                    for name in names:
                        connection.sendall(name.encode('ascii'))
                    dataa=connection.recv(1024)
                    dataa=dataa.decode()
                    dataa=dataa.split(':  ')
                    recievername=dataa[1]
                    sendername=dataa[0]
                    a=names.index(recievername)
                    recieversocket=clients[a]
                    msgg=sendername+'USER REQUEST YOU FOR PRIVATECHAT ENTER /YES OR /NO PLZ'
                    recieversocket.sendall(msgg.encode('ascii'))
                    while True:
                        dataa=recieversocket.recv(1024)
                        dataa=dataa.decode()
                        dataa=dataa.split(':  ')
                        dataa=dataa[1]
                        if dataa=='/YES':
                            connection.sendall('YOUR PRIVATE CHAT REQUEST IS ACCEPTED'.encode('ascii'))
                            connection.sendall('YOU HAVE JOINED PRRIVATE CHAT MODE'.encode('ascii'))
                            recieversocket.sendall('YOU HAVE JOINED PRRIVATE CHAT MODE'.encode('ascii'))
                            solo1=threading.Thread(target=AR, args=(connection,recieversocket))
                            solo1.start()
                            solo2=threading.Thread(target=AR, args=(recieversocket,connection))
                            solo2.start()
                            kill_thread=True
                            break
                        elif dataa=='/NO':
                            break
                        else:
                            recieversocket.sendall('WRONG INPUT ONLY /YES OR /NO INPUT CAN BE PASS'.encode('ascii'))
                else:
                    try:
                        x=clients.index(connection)
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
            for name in names:
                print(name)
        elif decison=='1':
            print('USERS LIST')
            for name in names:
                print(name)
            n=input('Wanna kick user ENTER THE NAME PLZ')
            index=names.index(n)
            con=clients[index]
            msg='USER '+n+' IS KICKED BY CHAT ROOM ADMIN'
            broadcast(msg.encode('ascii'),con)
            names.remove(n)
            clients.remove(con)
            msg='KICKED'
            con.sendall(msg.encode('ascii'))
t=threading.Thread(target=kick)
t.start()
listner(server)
