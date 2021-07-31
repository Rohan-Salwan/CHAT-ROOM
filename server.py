import threading
import socket

HOST=''
PORT=1231
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
