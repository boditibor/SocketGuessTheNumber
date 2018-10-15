import socket
import struct
import sys


class SimpleTCPSelectClient:
    def __init__(self, serverAddr='localhost', serverPort=10001):
        self.setupClient(serverAddr, serverPort)

    def setupClient(self, serverAddr, serverPort):
        server_address = (serverAddr, serverPort)

        # Create a TCP/IP socket
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        self.client.connect(server_address)

    def handleIncomingMessageFromRemoteServer(self):
        data = self.client.recv(4096)
        if data == "win":
            print data
            sys.exit()
        if data == "end":
            print data
            sys.exit()
        if not data:
            print '\nDisconnected from server'
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
                self.client.send(packed_data)
            self.handleIncomingMessageFromRemoteServer()


simpleTCPSelectClient = SimpleTCPSelectClient()
simpleTCPSelectClient.handleConnection()
