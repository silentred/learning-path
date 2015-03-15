#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import argparse, socket, IN

if not hasattr(IN, 'IP_MTU'):
    raise RuntimeError('cannot perform MTU discovery on this combination of OS and Python distribution')

def send_big_datagram(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.IPPROTO_IP, IN.IP_MTU_DISCOVER, IN.IP_PMTUDISC_DO)
    sock.connect((host, port))
    try:
        sock.send(b'#'*650000)
    except socket.error:
        print 'Alasm, datagram did not make it'
        max_mtu = sock.getsockopt(socket.IPPROTO_IP, IN.IP_MTU)
        print 'Actual MTU: {}'.format(max_mtu)
    else:
        print 'big datagram was sent'

if __name__ == '__main__' :
    parser = argparse.ArgumentParser(description='Send and recieve UDP locally')
    parser.add_argument('host', help='interface the server listens at')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060, help='UDP port (default 1060)')
    args = parser.parse_args()
    send_big_datagram( args.host, args.p)

