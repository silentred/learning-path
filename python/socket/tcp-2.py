#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import argparse, socket, sys
from datetime import datetime

def server(interface, port, bytecount):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((interface, port))
    sock.listen(1)
    print 'Listening at {}'.format(sock.getsockname())
    while True:
        sc, sockname = sock.accept()
        print 'Processing up to 1024 bytes at a time from', sockname
        n = 0
        while True:
            data = sc.recv(1024)
            if not data:
                break
            output = data.decode('ascii').upper().encode('ascii')
            sc.sendall(output)
            n += len(data)
            print '\r %d bytes processed so far ' % (n,)
            sys.stdout.flush()
        print ''
        sc.close()
        print 'socket closed'

def client(host, port, bytecount):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bytecount = bytecount + 32
    message = b'capitalize this!'
    print 'sending ', bytecount, 'byte of data, in chunks of 16 bytes'
    sock.connect((host, port))
    sent = 0
    while sent < bytecount:
        sock.sendall(message)
        sent += len(message)
        print '\r %d bytes sent' % (sent, )
        sys.stdout.flush()
    print ''
    sock.shutdown(socket.SHUT_WR)
    print 'Receving all the data the server sends back'
    recieved = 0
    while True:
        data = sock.recv(42)
        if not recieved:
            print 'The firest data recieved says', repr(data)
        if not data:
            break
        recieved += len(data)
        print '\r %d bytes recieved' % (recieved, )
    print ''
    sock.close()


if __name__ == '__main__' :
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Send and recieve TCP locally')
    parser.add_argument('role', choices=choices, help='which role to play')
    parser.add_argument('host', help='interface')
    parser.add_argument('bytecount', type=int, nargs='?', default=16 , help='bytes for client to send (default 16)')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060, help='UDP port (default 1060)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p, args.bytecount)

