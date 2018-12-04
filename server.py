import operator
import select
import socket
import sys
import struct


class SimpleTCPSelectServer:
    solved = False
    clients = []
    packages = ["csomag1 haz1", "csomag2 haz1", "csomag3 haz1", "csomag4 haz2", "csomag5 haz2", "csomag6 haz2"]

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

    def handleDataFromClient(self, sock):
            clientOnline = True
            try:
                data = sock.recv(1024)
                data = data.strip()
            except socket.error:
                print 'Client was closed!'
                clientOnline = False
            if clientOnline and data:
                unpacker = struct.Struct('i')
                unpacked_data = unpacker.unpack(data)
                if unpacked_data[0] == 1:
                    if len(self.packages) < 1:
                        sock.send('Out of package')
                    else:
                        package = self.packages[len(self.packages)-1]
                        self.packages.remove(self.packages[len(self.packages)-1])
                        packed_data = struct.pack("{}s".format(len(package)), package)
                        sock.send(packed_data)
                elif unpacked_data[0] == 2:
                    if len(self.packages) < 2:
                        sock.send('Out of package')
                    else:
                        package = self.packages[len(self.packages)-1] + ' ' + self.packages[len(self.packages)-2]
                        self.packages.remove(self.packages[len(self.packages)-1])
                        self.packages.remove(self.packages[len(self.packages)-1])
                        packed_data = struct.pack("{}s".format(len(package)), package)
                        sock.send(packed_data)
                elif unpacked_data[0] == 3:
                    if len(self.packages) < 3:
                        sock.send('Out of package')
                    else:
                        package = self.packages[len(self.packages)-1] + ' ' + self.packages[len(self.packages)-2] +\
                                  ' ' + self.packages[len(self.packages)-3]
                        self.packages.remove(self.packages[len(self.packages)-1])
                        self.packages.remove(self.packages[len(self.packages)-1])
                        self.packages.remove(self.packages[len(self.packages)-1])
                        packed_data = struct.pack("{}s".format(len(package)), package)
                        sock.send(packed_data)

            else:
                # Interpret empty result as closed connection
                print >> sys.stderr, 'closing', sock.getpeername(), 'after reading no data'
                # Stop listening for input on the connection
                self.inputs.remove(sock)
                sock.close()

    def handleInputs(self, readable):
        for sock in readable:
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
