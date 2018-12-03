import socket
import struct
import sys
import time


class SimpleTCPSelectClient:
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
        if data == "win":
            print data
            sys.exit()
        if data == "end":
            print data
            sys.exit()
        else:
            print data

    def handleConnection(self):
        while True:
            msg = raw_input('Message: ')
            if msg != '':
                values = (msg[0], int(msg[1:]))
                print values
                packer = struct.Struct('cH')
                packed_data = packer.pack(*values)
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
