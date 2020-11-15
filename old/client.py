import socket, threading, sys
from getopt import getopt
testmessage = '5         ' + '0         ' + 'James'
def sender(address):
    while True:
        message = testmessage
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(address)
            s.sendall(message.encode())


def start():
    o = dict(getopt(sys.argv[1:], 'h:p:l:')[0])
    threading.Thread(target=sender, args=(('127.0.0.1', int(o.get('-p',2223))),)).start()

if __name__ == "__main__":
    start()