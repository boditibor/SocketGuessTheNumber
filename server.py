import operator
import select
import socket
import sys
import struct
from random import randint


class SimpleTCPSelectServer:
    randomNumber = randint(1, 100)
    solved = False
    clients = []

    def __init__(self, addr='localhost', port=10001, timeout=1):
        self.server = self.setupServer(addr, port)
        # Sockets from which we expect to read
        self.inputs = [self.server]
        # Wait for at least one of the sockets to be ready for processing
        self.timeout = timeout

    def setupServer(self, addr, port):
        # Create a TCP/IP socket
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setblocking(0)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind the socket to the port
        server_address = (addr, port)
        server.bind(server_address)

        # Listen for incoming connections
        server.listen(5)
        return server

    def handleNewConnection(self, sock):
        # A "readable" server socket is ready to accept a connection
        connection, client_address = sock.accept()
        connection.setblocking(0)  # or connection.settimeout(1.0)
        self.inputs.append(connection)

    def applyOp(self, in1, op, in2):
        ops = {'<': operator.lt, '>': operator.gt, '=': operator.eq}
        return ops[op](in1, in2)

    def handleDataFromClient(self, sock):
        data = sock.recv(1024)
        data = data.strip()
        if data:
            print self.randomNumber
            unpacker = struct.Struct('cH')
            unpacked_data = unpacker.unpack(data)
            print 'Unpacked data:', unpacked_data
            bool = self.applyOp(self.randomNumber, unpacked_data[0], unpacked_data[1])
            if unpacked_data[0] == '<' or unpacked_data[0] == '>':
                if bool:
                    sock.send("yes")
                else:
                    sock.send("no")
            if unpacked_data[0] == '=':
                if bool:
                    sock.send("win")
                    print "Close the system"
                    for c in self.clients:
                        if c != sock:
                            c.send("end")
                            c.shutdown(socket.SHUT_RDWR)
                            c.close()
                    self.inputs = []
                else:
                    sock.send("no")
        else:
            # Interpret empty result as closed connection
            print >> sys.stderr, 'closing', sock.getpeername(), 'after reading no data'
            # Stop listening for input on the connection
            self.inputs.remove(sock)
            sock.close()

    def handleInputs(self, readable):
        for sock in readable:
            print sock
            if sock is self.server:
                self.handleNewConnection(sock)
            else:
                self.clients.append(sock)
                self.handleDataFromClient(sock)

    def handleExceptionalCondition(self, exceptional):
        for sock in exceptional:
            print >> sys.stderr, 'handling exceptional condition for', sock.getpeername()
            # Stop listening for input on the connection
            self.inputs.remove(sock)
            sock.close()

    def handleConnections(self):
        while self.inputs:
            try:
                readable, writable, exceptional = select.select(self.inputs, [], self.inputs, self.timeout)

                if not (readable or writable or exceptional):
                    # print >>sys.stderr, '  timed out, do some other work here'
                    continue

                self.handleInputs(readable)
                self.handleExceptionalCondition(exceptional)
            except KeyboardInterrupt:
                print "Close the system"
                for c in self.inputs:
                    c.close()
                self.inputs = []


simpleTCPSelectServer = SimpleTCPSelectServer()
simpleTCPSelectServer.handleConnections()
