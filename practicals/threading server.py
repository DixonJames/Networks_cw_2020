import socket
import threading
import sys
from getopt import getopt
My_address = ("127.0.0.1", 2222)
def receiver(address):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = ('localhost', 10000)
    print('starting up on {} port {}'.format(*server_address))
    sock.bind(server_address)

    sock.listen(1)

    while True:

        print('waiting for a connection')
        connection, client_address = sock.accept()
        try:
            print('connection from', client_address)

            while True:
                data = connection.recv(16)
                print('received {!r}'.format(data))
                if data:
                    print('sending data back to the client')
                    connection.sendall(data)
                else:
                    print('no data from', client_address)
                    break

        finally:

            connection.close()



if __name__ == '__main__':
    receiver(My_address)


