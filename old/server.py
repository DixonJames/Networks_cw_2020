import socket, threading, sys, select
from getopt import getopt
clients =[]
def receiver(address):
    with socket.socket() as s:
        s.bind(address)
        while True:
            connection, (peer_ip, _) = s.accept()
            with connection:
                message = connection.recv(1024).decode()
                print("{}: {}".format(peer_ip, message))

def listenNewUsers(socket):
    while True:
        try:
            new_clinet = socket.listen(1)
            if new_clinet not in clients:
                clients.append(new_clinet)
        except:
            continue

def start():
    o = dict(getopt(sys.argv[1:], 'h:p:l:')[0])
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    threading.Thread(target=listenNewUsers, args=(('', int(o.get('-l', 2223))),)).start()
    threading.Thread(target=receiver, args=(('', int(o.get('-l',2223))),)).start()


if __name__ == "__main__":
    start()

