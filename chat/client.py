import socket, sys
from threading import Thread

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print('Failed to create socket')
    sys.exit()

def echo():
    msg = input('Enter message to send : ')
    try:
        sock.sendto(msg.encode('utf-8'), (host, port))
        reply, addr = sock.recvfrom(1024)
        if reply:
            print(reply.decode('utf-8'))
    except socket.error:
        print('Some error...')
        sys.exit()
 
host = 'localhost'
port = 8888
thr = None
while 1:  
    if not thr:
        thr = Thread(target=echo)
        thr.start()
    else:
        print(thr.daemon)
        if thr.daemon:
            print('asd')
            thr = None
    try:
        reply, addr = sock.recvfrom(1024)
        if reply:
            print(reply.decode('utf-8'))
    except:
        continue
