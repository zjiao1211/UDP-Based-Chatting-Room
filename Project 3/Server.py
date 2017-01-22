#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Programming Assignment 3 - Server

import socket
import threading
import time

def tcplink(sock, addr):
    print 'Accept new connection from %s:%s...' % addr
    i = 1
    while True:
        data = sock.recv(1000)
        if len(data) == 1000:
            total = str(1000 * i)
            port = str(addr[1])
            print 'Received 1000 bytes from '+addr[0]+':'+port+'. Total: ' + total
        else:
            break
        i = i + 1
        time.sleep(1)
        if data == 'exit' or not data:
            break
    sock.close()
    print 'Connection from %s:%s closed.' % addr

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 9999))
s.listen(5)
print 'Waiting for connection...'

while True:
    sock, addr = s.accept()
    t = threading.Thread(target=tcplink, args=(sock, addr))
    t.start()
