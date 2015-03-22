#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import argparse, socket
from datetime import datetime

def recvall(sock, length):
    data = b''
    while len(data) < length:
        data = sock.recv(length - len(data))
        if not data:
            raise EOFError('was exprect %d bytes but only recieved %d bytes before the socket closed' % (length, len(data)))
    return data

def server(interface, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((interface, port))
    sock.listen(1)
    print 'Listening at {}'.format(sock.getsockname())
    while True:
        sc, sockname = sock.accept()
        print 'We have accepted a connection from', sockname
        print 'Socket name: ', sc.getsockname()
        print 'Socket peer : ', sc.getpeername()
        message = recvall(sc, 16)
        print 'Incoming 16 message: ', repr(message)
        sc.sendall(b'Farewell, client !!!@@@')
        sc.close()
        print 'Reply sent, socket closed'

def client(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print 'Client has been assigned socket name', sock.getsockname()
    sock.sendall(b'Hi there,  server !!!!@@@####$$$%^^')
    reply = recvall(sock, 16)
    print 'The server said', repr(reply)
    sock.close()



if __name__ == '__main__' :
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Send and recieve TCP locally')
    parser.add_argument('role', choices=choices, help='which role to play')
    parser.add_argument('host', help='interface')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060, help='UDP port (default 1060)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)

