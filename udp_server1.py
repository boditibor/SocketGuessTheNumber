import random
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ("localhost", 10000)
sock.bind(server_address)

packages = []

while True:
	text, client = sock.recvfrom(1024)
	tmp = text.split(' ')
	print tmp[0]
	print tmp[1]
	print tmp[1][0:5]
	if tmp[1][0:6] == "csomag":
		packages.append(tmp[1])
		print(packages)
		sock.sendto('Got the package! ' + str(tmp[1]), client)

sock.close()

