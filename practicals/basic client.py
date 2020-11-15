import socket
import threading
import sys
from getopt import getopt
My_address = ("127.0.0.1", 2222)

def sender(addres):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 10000)
    print('connecting to {} port {}'.format(*server_address))
    sock.connect(server_address)
    while True:
        try:

            # Send data
            message = str(input(">>"))
            print('sending {!r}'.format(message))
            sock.sendall(message.encode())

            # Look for the response
            amount_received = 0
            amount_expected = len(message)

            while amount_received < amount_expected:
                data = sock.recv(16)
                amount_received += len(data)
                print('received {!r}'.format(data))

        except:
            print("closed connection")
            sock.close()



sender(My_address)