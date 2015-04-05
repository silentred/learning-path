#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import socket

if __name__ == '__main__':
    hostname = 'www.python.org'
    addr = socket.gethostbyname(hostname)
    print 'The ip address of {} is {}'.format(hostname, addr)

