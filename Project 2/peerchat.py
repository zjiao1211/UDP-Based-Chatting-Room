#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Programming Assignment 2 第五题终极版

import socket
import select
import sys
import re

global check
check = 1
global check2
check2 = 1
global check3
check3 = 1
global check4
check4 = 1
global t
t = 1

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
data = 'SRC:000;DST:999;PNUM:1;HCT:1;MNUM:100;VL:;MESG:register'
print 'The message for a registration request is:', data
s.sendto(data, ('steel.isi.edu', 63682))
recv = s.recv(1024)
print 'The server’s response is:', recv
back = re.split(r'[:;]\s*', recv)
if back[5] == '0':
    print back[13]
elif back[5] == '2':
    print 'Successfully registered. My ID is: ', back[3]

while True:
    readlist = [sys.stdin, s]
    rlist, wlist, elist = select.select(readlist, [], [], 1)
    if not (rlist or wlist or elist):
        if check == 0 and check3 == 1: #说明此是msg后等ACK
            if t < 5:
                print "No ACK, so retry messages! "
                t = t + 1
                s.sendto(data3, (IP, Port))
            elif t == 5:
                print '********************'
                print 'ERROR: Gave up sending to ' + dst
                print '********************'
                t = 1
                check = 1
        elif check2 == 0:#说明此是all后等ACK
            k = 0
            for time in v:
                if time < 5:
                    print 'No ACK from '+Registry3[3*k]+', so retry messages! '
                    v[k] = v[k] + 1
                    data_re = 'SRC:' + back[3] + ';DST:' + Registry3[3*k] + ';PNUM:7;HCT:1;MNUM:103;VL:;MESG:' + message
                    IP = Registry3[3*k+1]
                    Port = int(Registry3[3*k+2])
                    s.sendto(data_re, (IP, Port))
                elif time == 5:
                    print 'ERROR: Gave up sending to ' + Registry3[3*k]
                    v[k] = 10
                k = k + 1
        elif check3 == 0:#说明此是发送端forward后等ACK
            kk = 0
            for time1 in n:
                if time1 < 5:
                    print 'No ACK from ' + Registry3[3 * kk] + ', so retry messages! '
                    n[kk] = n[kk] + 1
                    data_relay = 'SRC:' + back[3] + ';DST:' + dst + ';PNUM:3;HCT:9;MNUM:102;VL:' + New_list + ';MESG:' + message
                    IP = Registry3[3 * kk + 1]
                    Port = int(Registry3[3 * kk + 2])
                    s.sendto(data_relay, (IP, Port))
                elif time1 == 5:
                    print 'ERROR: Gave up sending to ' + Registry3[3 * kk]
                    n[kk] = 10
                kk = kk + 1
        elif check4 == 0:#说明此是中间人forward后等ACK
            kkk = 0
            for time2 in e:
                if time2 < 5:
                    print 'No ACK from ' + Registry3[3 * kkk] + ', so retry messages! '
                    e[kkk] = e[kkk] + 1   #messsage改成收到的信息
                    data_relay = 'SRC:' + back3[1] + ';DST:' + back3[3] + ';PNUM:3;HCT:'+back3[7]+';MNUM:'+back3[9]+';VL:' + New_list + ';MESG:' + back3[13]
                    IP = Registry3[3 * kkk + 1]
                    Port = int(Registry3[3 * kkk + 2])
                    s.sendto(data_relay, (IP, Port))
                elif time2 == 5:
                    print 'ERROR: Gave up sending to ' + Registry3[3 * kkk]
                    e[kkk] = 10
                kkk = kkk + 1
    for sock in rlist:
        #从socket里面读数据,说明此时要接收信息
        if sock == s:
            recv3, addr3 = s.recvfrom(1024)
            recv3_1 = re.split(r'[:;]\s*', recv3)
            # 正常数据接收并返回ACK
            if recv3_1[5] == '3' and recv3_1[3] == back[3]:
                print 'A message arrives: ', recv3
                back3 = re.split(r'[:;]\s*', recv3)
                ACK = 'SRC:' + back[3] + ';DST:' + back3[1] + ';PNUM:4;HCT:1;MNUM:' + back3[9] + ';VL:;MESG:ACK'
                s.sendto(ACK, addr3)
                print 'Send a ACK to confirm: ' + ACK
                break

            # 作为中间人收到Forward packet,然后返回ACK,分情况转发
            elif recv3_1[5] == '3' and recv3_1[3] != back[3]:
                check4 = 0
                back3 = re.split(r'[:;]\s*', recv3)
                ACK = 'SRC:' + back3[3] + ';DST:' + back3[1] + ';PNUM:4;HCT:1;MNUM:' + back3[9] + ';VL:'+recv3_1[11]+';MESG:ACK'
                print ACK
                s.sendto(ACK, addr3)
                print 'Receive a forward packet from ' + back3[1]
                print 'Current VL:' + recv3_1[11]
                if back3[7] == '0':
                    print '********************'
                    print 'Dropped message from '+back3[1]+'to '+ back3[3]+' - hop count exceeded'
                    print 'MESG: '+ back3[13]
                elif back3[7] != '0':
                    New_list = re.split(r'[,]\s*', back3[11])
                    if back[3] in back3[11]:
                        print '********************'
                        print 'Dropped message from ' + back3[1] + 'to ' + back3[3] + ' - peer revisited'
                        print 'MESG: ' + back3[13]
                    elif back[3] not in back3[11]:
                        for x in Registry3[::3]:
                            if x == back[3]:
                                index = Registry3.index(back[3])
                                Registry3.remove(Registry3[index])
                                Registry3.remove(Registry3[index])
                                Registry3.remove(Registry3[index])
                        e = [1 for x in range(0, 3)]
                        back3[7] = int(back3[7]) - 1
                        back3[7] = str(back3[7])
                        New_list.append(back[3])
                        New_list = ','.join(New_list)
                        data_relay = 'SRC:' + back3[1] + ';DST:' + back3[3] + ';PNUM:3;HCT:'+back3[7]+';MNUM:' + back3[9] + ';VL:'+ New_list+';MESG: '+ back3[13]
                        print 'Current VL:' + New_list
                        print 'And forward the packet to: ',
                        for u in range(0, 3):
                            IP = Registry3[3 * u + 1]
                            Port = int(Registry3[3 * u + 2])
                            print Registry3[3 * u],
                            s.sendto(data_relay, (IP, Port))
                        print ''

            #我forward给别人,然后别人给我ACK确认
            elif check3 == 0 and recv3_1[5] == '4' and recv3_1[3] == back[3] and recv3_1[7] == '1':
                for relay in range(0, 3):
                    if (Registry3[3*relay+1] in addr3) and (Registry3[relay+1] in addr3):
                        print Registry3[3 * relay] + ' successfully receive my forwarding packet!'
                        n[relay] = 10
                        print relay
                        print n[relay]
                        break

            elif check4 == 0 and recv3_1[5] == '4':  # 说明此是中间人forward后等ACK
                for relay2 in range(0, 3):
                    if (Registry3[3 * relay2 + 1] in addr3) and (Registry3[relay + 1] in addr3):
                        m = relay2
                        break
                print Registry3[3 * m] + ' successfully receive my forwarding packet!'
                e[m] = 10

            elif recv3_1[5] == '7' and recv3_1[3] == back[3]: #说明此是收到广播后发ACK
                print '********************'
                print 'SRC:  '+recv3_1[1]+' broadcasted:'+recv3_1[13]
                ACK = 'SRC:' + back[3] + ';DST:' + recv3_1[1] + ';PNUM:8;HCT:1;MNUM:' + recv3_1[9] + ';VL:;MESG:ACK'
                s.sendto(ACK, addr3)
                print 'Send a ACK to confirm the broadcast from: ' + recv3_1[1]

            elif check == 0 and t < 5:  #说明此是msg后等ACK
                if data3_2[1] == recv3_1[3] and data3_2[3] == recv3_1[1] and recv3_1[5] == '4' and recv3_1[13] == 'ACK':
                    print 'Successfully received ACK from '+recv3_1[1]
                    check = 1
                    t = 1
                    break
                else:
                    t = t + 1
                    s.sendto(data3, (IP, Port))

            elif check2 == 0:   #说明此是all后等ACK
                if recv3_1[5] == '8' and recv3_1[3] == back[3] and recv3_1[9] == '103':
                    print 'Successfully received ACK from '+recv3_1[1]
                    v[(Registry3.index(recv3_1[1]))/3] = 10
                else:
                    print 'Wrong ACK'
                    q = (Registry3.index(recv3_1[1]))/3
                    v[q] = v[q] + 1
                    data_re = 'SRC:' + back[3] + ';DST:' + Registry3[3 * q] + ';PNUM:7;HCT:1;MNUM:103;VL:;MESG:' + message
                    IP = Registry3[3 * q + 1]
                    Port = int(Registry3[3 * q + 2])
                    s.sendto(data_re, (IP, Port))
            else:
                print 'I do not know the mean of the message I receive'

        #从stdin里面读数据,说明此时要键入命令
        elif sock == sys.stdin:
            command = sys.stdin.readline()
            command  = command.lower()
            #开始进行数据传输
            if command == 'msg'+'\n':
                dst = raw_input('Please input your dst: ')
                dst = int(dst)
                dst = '{0:03d}'.format(dst)
                message = raw_input('Please input your message: ')
                check = 0
                if len(message) > 200:
                    message = message[0:200]
                data3 = 'SRC:' + back[3] + ';DST:' + dst + ';PNUM:3;HCT:1;MNUM:102;VL:;MESG:' + message
                print 'We sent a message: '+ data3
                #分两种情况讨论
                if dst in Registry3:#有地址我就发送
                    IP = Registry3[Registry3.index(dst) + 1]
                    Port = int(Registry3[Registry3.index(dst) + 2])
                    data3_2 = re.split(r'[:;]\s*', data3)
                    t = 1
                    s.sendto(data3, (IP, Port))
                else:#没地址我就转发给三个人
                    print 'Cannot find ' + dst + ' in my Registry. So I forward it to:',
                    check3 = 0
                    for x in Registry3[::3]:
                        if x == back[3]:
                            index = Registry3.index(back[3])
                            Registry3.remove(Registry3[index])
                            Registry3.remove(Registry3[index])
                            Registry3.remove(Registry3[index])
                    n = [1 for x in range(0, 3)]
                    data_relay = 'SRC:' + back[3] + ';DST:' + dst + ';PNUM:3;HCT:9;MNUM:102;VL:;MESG:' + message
                    data_relay_1 = re.split(r'[:;]\s*', data_relay)
                    New_list = re.split(r'[,]\s*', data_relay_1[11])
                    New_list.append(back[3])
                    New_list = ''.join(New_list)
                    data_relay = 'SRC:' + back[3] + ';DST:' + dst + ';PNUM:3;HCT:9;MNUM:102;VL:' + New_list + ';MESG:' + message
                    for u in range(0, 3):
                        relayto = Registry3[3 * u]
                        print relayto,
                        IP = Registry3[3 * u + 1]
                        Port = int(Registry3[3 * u + 2])
                        s.sendto(data_relay, (IP, Port))
                    print ''

            #开始进行查表
            elif command == 'ids'+'\n':
                data2 = 'SRC:' + back[3] + ';DST:999;PNUM:5;HCT:1;MNUM:101;VL:;MESG:get map'
                print 'The message to request the registry is:', data2
                s.sendto(data2, ('steel.isi.edu', 63682))
                recv2 = s.recv(1024)
                back2 = re.split(r'[:;]\s*', recv2)
                if back2[5] == '0':
                    print back2[13]
                elif back2[5] == '6':
                    print '********************'
                    print 'Recently Seen Peers:'
                    Registry = re.split(r'and', back2[13])
                    Registry2 = re.split(r'[,=]', Registry[0])
                    Registry3 = re.split(r'[,=@]', Registry[1])
                    print ','.join(Registry2[1:len(Registry2)])
                    print '\n'
                    print 'Known addresses:'
                    i = 1
                    for c in Registry3:
                        if i % 3 == 0:
                            print c + '\n',
                        else:
                            print c + ' ',
                        i = i + 1
                    print '********************'

            #开始进行广播
            elif command == 'all' + '\n':
                message = raw_input('Please input your message: ')
                if len(message) > 200:
                    message = message[0:200]
                remove = 0
                for x in Registry3[::3]:
                    if x == back[3]:
                        index = Registry3.index(back[3])
                        Registry3.remove(Registry3[index])
                        Registry3.remove(Registry3[index])
                        Registry3.remove(Registry3[index])
                        remove = remove + 1
                v = [1 for x in range(0, (len(Registry3[::3]) - remove))]
                check2 = 0
                for y in Registry3[::3]:
                    dst = y
                    IP = Registry3[Registry3.index(dst) + 1]
                    Port = int(Registry3[Registry3.index(dst) + 2])
                    data4 = 'SRC:' + back[3] + ';DST:' + dst + ';PNUM:7;HCT:1;MNUM:103;VL:;MESG:' + message
                    s.sendto(data4, (IP, Port))
            else:
                print 'Command is invalid'