#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Programming Assignment 1

import argparse
import socket

def connect():
  HOST, PORT = "eig.isi.edu", 63681
  try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST,PORT))
    sock.settimeout(3)
    return sock
  except Exception as e:
    print("Server may be down!! Please send email.")
    print(e)
    return None

def send(s, message):
  try:
    s.sendall(message.encode('utf-8'))
  except Exception as e:
    print(e)

def recv(s):
  try:
    data = s.recv(1024)
    if len(data) == 0:
            print("Connection ended by server.")
    print("Recieved message from server: \"%s\"" %(data))
    return data.decode('utf-8')
  except socket.timeout:
    print("No messages received from the server.")
    print("Maybe the server *did not* get your message!")
    print("Or maybe you sent a non-protocol message and the server has no response.")
    return "TIMEOUT"
  except Exception as e:
    print(e)
    return "ERROR"

class FSM(object):
    crtst = ''

def reconnect():
    send(s, 'hi')
    data = recv(s)
    while data != 'hello':
        send(s, 'hi')
        data = recv(s)
    print('New connection established!!!!!!!')
    JZ.crtst = 'C'

if __name__ == "__main__":
  # Set up argument parsing.
  parser = argparse.ArgumentParser(description='EE450 Programming Assignment #1')
  parser.add_argument('commands',  nargs='+', help='Space eliminated commands')
  args = parser.parse_args()

JZ = FSM()
JZ.crtst = 'idle'
Getd = 0
i = 0
while args.commands != ' ' and JZ.crtst == 'idle':
    s = connect()
    if s == None:
        exit()
    else:
        send(s, 'hi')
        data = recv(s)
        while(data != 'hello'):
            send(s, 'hi')
            data = recv(s)
        print('Connection established!!!!!!!')
        JZ.crtst = 'C'
for command in args.commands:
    i = i + 1
    if command == 'b' and JZ.crtst == 'C':
        JZ.crtst='C1'
        send(s, 'banana')
        data = recv(s)
        while data != "yellow":
            print ('Not a valid response, then resend the command')
            send(s, 'banana')
            data = recv(s)
    elif command == 'r' and JZ.crtst == 'C1':
        JZ.crtst='C'
        send(s, 'rose')
        data = recv(s)
        while data != "red":
            print ('Not a valid response, then resend the command')
            send(s, 'rose')
            data = recv(s)
    elif command == 'g' and JZ.crtst == 'C':
        JZ.crtst='C2'
        send(s, 'grass')
        data = recv(s)
        while data != "green":
            print ('Not a valid response, then resend the command')
            send(s, 'grass')
            data = recv(s)
    elif command == 'v' and JZ.crtst == 'C2':
        JZ.crtst='C3'
        send(s, 'violets')
        data = recv(s)
        while data != "purple":
            print ('Not a valid response, then resend the command')
            send(s, 'violets')
            data = recv(s)
    elif command == 'f' and JZ.crtst == 'C3':
        JZ.crtst='C'
        send(s, 'fish')
        data = recv(s)
        while data != "gold":
            print ('Not a valid response, then resend the command')
            send(s, 'fish')
            data = recv(s)
    elif command == 's' and JZ.crtst == 'C':
        JZ.crtst='C3'
        send(s, 'sky')
        data = recv(s)
        while data != "blue":
            print ('Not a valid response, then resend the command')
            send(s, 'sky')
            data = recv(s)
    elif command == 'd':
        JZ.crtst='F'
        Getd = 1
        send(s, 'done')
        data = recv(s)
        while data != "cya":
            print ('Not a valid response, then resend the command')
            send(s, 'cya')
            data = recv(s)
        send(s, 'bye')
        print('Connection over!!!!!!!')
        JZ.crtst='idle'
        if i < len(args.commands):
            reconnect()
            Getd = 0
        else:
            print('No more connections')
    else:
        print ('Command ' + command + ' does not following the protocol or it is not known')
        continue
if Getd == 0:
    print("Automatically send command d")
    send(s, 'done')
    data = recv(s)
    while data != 'cya':
            print ('Not a valid response, then resend the command')
            send(s, 'done')
            data = recv(s)
    JZ.crtst='F'
    send(s, 'bye')
    print('Connection over!!!!!!!')
    JZ.crtst='idle'
print("The ultimate state is: \"%s\"" %(JZ.crtst))


