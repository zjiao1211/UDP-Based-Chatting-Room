#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Programming Assignment 3 - Client

import socket
import random

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 9999))
length = random.randint(2000, 10000)
leng = str(length)
print 'Send an amount of data to the server:' + leng
data = ''.join(['0' for x in range(0, length)])
s.send(data)
s.send('exit')
s.close()