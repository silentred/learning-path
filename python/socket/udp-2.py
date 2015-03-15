#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import argparse, socket, random, sys
from datetime import datetime

MAX_BYTES=65535

def server(interface, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((interface, port))
    print 'Listening at {}'.format(sock.getsockname())
    while True:
        data, address = sock.recvfrom(MAX_BYTES)
        if random.random() < 0.5:
            print "Pretending to drop packet from {}".format(address)
            continue
        text = data.decode('ascii')
        print 'The client at {} says {!r}'.format(address, text)
        text = 'Your data was {} bytes long'.format(len(data))
        data = text.encode('ascii')
        sock.sendto(data, address)

def client( interface, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    hostname = sys.argv[2]
    sock.connect((hostname, port))
    print 'Client socket name is {}'.format(sock.getsockname())

    delay = 0.1
    text = 'This is another message'
    data = text.encode('ascii')
    while True:
        sock.send(data)
        print 'Waiting up to {} seconds for a reply'.format(delay)
        sock.settimeout(delay)
        try:
            data = sock.recv(MAX_BYTES)
        except socket.timeout:
            delay *= 2
            if delay > 2.0:
                raise RuntimeError('I think the server is down')
        else:
            break
    print 'The server says {!r}'.format(data.decode('ascii'))


if __name__ == '__main__' :
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Send and recieve UDP locally')
    parser.add_argument('role', choices=choices, help='which role to play')
    parser.add_argument('host', help='interface the server listens at')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060, help='UDP port (default 1060)')
    args = parser.parse_args()
    function = choices[args.role]
    function( args.host, args.p)

