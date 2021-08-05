import threading
import socket

HOST=''
PORT=1260
server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST,PORT))
server.listen()
print('CHATROOM SERVER IS ACTIVATED')
clients=[]
names=[]
def listner(server):
    while True:
        conn, addr=server.accept()
        print('CONNECTED TO', addr)
        clients.append(conn)
        conn.sendall('YOU HAVE JOINDED THE CHATROOM'.encode('ascii'))
        name=conn.recv(1024)
        name=name.decode()
        altering=name.split(':  ')
        name=altering[0]
        names.append(name)
        decision=altering[1]
        if decision=='/PRIVATECHAT':
            conn.sendall('SELECT TNE NAME FROM LIST WHOME TOU WANNA CHAT PRIVATE AND TYPE IT'.encode('ascii'))
            for name in names:
                conn.sendall(name.encode('ascii'))
            dataa=conn.recv(1024)    
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
                    conn.sendall('YOUR PRIVATE CHAT REQUEST IS ACCEPTED'.encode('ascii'))
                    conn.sendall('YOU HAVE JOINED PRRIVATE CHAT MODE'.encode('ascii'))
                    recieversocket.sendall('YOU HAVE JOINED PRRIVATE CHAT MODE'.encode('ascii'))
                    while True:
                        solo1=threading.Thread(target=AR, args=(conn,recieversocket))
                        solo1.start()
                        solo2=threading.Thread(target=AR, args=(recieversocket,conn))
                        solo2.start()
                elif dataa=='/NO':
                    break
                else:
                    recieversocket.sendall('WRONG INPUT ONLY /YES OR /NO INPUT CAN BE PASS'.encode('ascii'))
        elif decision=='/PUBLICCHAT':
            ta=threading.Thread(target=reciever, args=(conn,))
            ta.start()
        else:
            pass

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
            data=connection.recv(1024)
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
