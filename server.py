import threading
import socket

HOST=''
PORT=1274
server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST,PORT))
server.listen()
print('CHATROOM SERVER IS ACTIVATED')
clients=[]
names=[]
solo=None
def listner(server):
    while True:
        conn, addr=server.accept()
        print('CONNECTED TO', addr)
        clients.append(conn)
        message='YOU HAVE JOINDED THE CHATROOM'
        conn.sendall(message.encode('ascii'))
        name=conn.recv(1024)
        names.append(name.decode())
        t=threading.Thread(target=reciever, args=(conn,))
        t.start()

def broadcast(message,ex):
    for client in clients:
        if client==ex:
            pass
        else:
            client.sendall(message)

def solochat(smsg,helper):
    helper.sendall(smsg)

def reciever(connection):
    while True:
        try:
            data=connection.recv(1024)
            if data.decode()=='/PRIVATECHAT':
                for name in names:
                    connection.sendall(name.encode('ascii'))
                connection.sendall('[SELECT THE USER FROM LIST & ENTER THE NAME PLZ]'.encode('ascii'))
                solodata=connection.recv(1024)
                solodata=solodata.decode()
                solodata=solodata.split(':  ')
                solodata=solodata[1]
                ab=names.index(solodata)
                recieverclient=clients[ab]
                ss=clients.index(connection)
                sendername=names[ss]
                sendername=sendername+'  REQUESTED YOU FOR PRIVATE CHAT TYPE YES OR NO'
                recieverclient.sendall(sendername.encode('ascii'))
                while True:
                    de=recieverclient.recv(1024)
                    de=de.decode()
                    de=de.split(':  ')
                    de=de[1]
                    if de =='YES':
                        connection.sendall('YOUR PRIVATE CHAT REQUEST IS ACCEPTED'.encode('ascii'))
                        #connection.sendall('YOU ARE NOW CONNECTED WITH'+solodata+'IN PRIVATE CHAT'.encode('ascii'))
                        recieverclient.sendall('YOU ARE NOW CONNECTED WITH IN PRIVATE CHAT'.encode('ascii'))
                        solo='/PRIVATECHAT'
                        break
                    elif de=='NO':
                        connection.sendall('YOUR PRIVATE CHAT REQUEST IS DECLINED BY'+solodata.encode('ascii'))
                        solo =None
                        break
                    else:
                        recieverclient.sendall('[WRONG INPUT] ONLY YES OR NO INPUTS ARE ALLOWED TO PASS'.encode('ascii'))
                        recieverclient.sendall(sendername+'REQUESTED YOU FOR PRIVATE CHAT TYPE YES OR NO')
            if solo=='/PRIVATECHAT':
                try:
                    recieverclient.sendall(data)
                except:
                    connection.close()
                    break
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
