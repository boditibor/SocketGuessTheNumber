import socket
import struct
import sys
import time
from random import randint


class SimpleTCPSelectClient:
    packets = []
    msg = ''

    def __init__(self, serverAddr='localhost', serverPort=10001):
        self.setupClient(serverAddr, serverPort)

    def setupClient(self, serverAddr, serverPort):
        server_address = (serverAddr, serverPort)

        # Create a TCP/IP socket
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        connected = False
        while not connected:
            try:
                self.client.connect(server_address)
                connected = True
            except socket.error:
                print 'Can not connect to the server!\n Reconnecting in 5 seconds!'
                time.sleep(5)
        print 'Connected to the Server!'

    def handleIncomingMessageFromRemoteServer(self):
        data = self.client.recv(4096)
        if not data:
            print '\nDisconnected from server'
            sys.exit()
        else:
            unpacked_data = struct.unpack("{}s".format(len(data)), data)
            if len(unpacked_data[0]) == 38:
                a,b,c,d,e,f = unpacked_data[0].split(' ')
                self.packets.append(a)
                self.packets.append(b)
                self.packets.append(c)
                self.packets.append(d)
                self.packets.append(e)
                self.packets.append(f)
                print self.packets
            elif len(unpacked_data[0]) == 25:
                a,b,c,d = unpacked_data[0].split(' ')
                self.packets.append(a)
                self.packets.append(b)
                self.packets.append(c)
                self.packets.append(d)
                print self.packets
            elif len(unpacked_data[0]) == 12:
                a, b = unpacked_data[0].split(' ')
                self.packets.append(a)
                self.packets.append(b)
                print self.packets
            else:
                print data

    def handleConnection(self):
        while self.msg != 'udp':
            print self.msg
            randomNumber = randint(1, 3)
            self.msg = raw_input('Message: ')
            if self.msg != '':
                print 'I would like to get ' + str(randomNumber) + ' package!'
                packer = struct.Struct('i')
                packed_data = packer.pack(randomNumber)
                try:
                    self.client.send(packed_data)
                except socket.error:
                    print 'Could not send the message to the Server!'
            try:
                self.handleIncomingMessageFromRemoteServer()
            except socket.error:
                print 'It seems to be unavailable!'


simpleTCPSelectClient = SimpleTCPSelectClient()
simpleTCPSelectClient.handleConnection()

tmpHaz = ''
for data in simpleTCPSelectClient.packets:
    tmpCsomag = data
    if data == 'haz1':
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            server_address = ("localhost", 10000)
            sock.sendto(tmpCsomag + ' ' + tmpHaz, server_address)
            answ = sock.recvfrom(1024)
            print(answ[0])
            sock.close()
        except socket.error:
            print 'UDP server seems to be not online!'
    else:
        tmpHaz = data








