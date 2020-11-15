import socket, threading, sys
from getopt import getopt

def receiver(address):
    with socket.socket() as s:
        s.bind(address)
        s.listen(1)
        while True:
            connection, (peer_ip, _) = s.accept()
            with connection:
                message = connection.recv(1024).decode()
                print("{}: {}".format(peer_ip, message))

def sender(address):
    while True:
        message = input(">> ")
        with socket.socket() as s:
            s.connect(address)
            s.sendall(message.encode())

def start():
    o = dict(getopt(sys.argv[1:], 'h:p:l:')[0])
    threading.Thread(target=receiver, args=(('', int(o.get('-l',8080))),)).start()
    threading.Thread(target=sender, args=(('127.0.0.1', int(o.get('-p',8080))),)).start()

if __name__ == "__main__":
    start()