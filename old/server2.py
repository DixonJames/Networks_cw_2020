import socket, threading, sys, select
from getopt import getopt


Header_size = 20
HOME_ip = '127.0.0.1'

socket_username = {}

class Room():
    def __init__(self, rm_number):
        self.Room_num = rm_number



        self.socket_username = {}

        try:
            self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            self.port_num = 2222 + rm_number
            self.socket_server.bind((HOME_ip, self.port_num))
        except:
            print("ERROR: setting up server failed")
        self.client_sockets = [self.socket_server]

    def portListen(self):
        """
        listening for new connections in the port + adding to list of connections
        """
        self.socket_server.listen()
        print(f'room:{self.Room_num} started listing on port {self.port_num}')

        connection, (peer_ip, _) = self.socket_server.accept()
        if connection not in self.client_sockets:
            self.client_sockets.append(connection)
            print(connection)


    def getMessage(self, client_socket):
        try:
            msg_header = client_socket.recv(Header_size)
            if len(msg_header) != Header_size:
                print(f'invalid message from {client_socket}')
                return False
            msg_size, msg_type = int(msg_header[:(len(msg_header)/2)]), str(msg_header[(len(msg_header)/2):])
            msg_content = client_socket.recv(msg_size)

            if not(msg_content):
                msg_content = None

            return {'type': msg_type.decode('utf-8'), 'content': msg_content.decode('utf-8')}

        except:
            print(f'error receiving from {client_socket}')
            return False

    def clientReceiver(self,active_socket):
        """

        :param active_socket: socket to active client
        :return:
        """
        print("")
        if active_socket == self.socket_server:

            new_client_socket, new_client_address = self.socket_server.accept()
            self.client_sockets.append(new_client_socket)

            message = self.getMessage(active_socket)

            if message['content'].decode() != None:
                new_client_nickname = message['content']
                print(f'new user : {new_client_nickname}')
            else:
                print(f'new user : {new_client_address}')

            self.client_directory[new_client_socket] = new_client_address

        else:
            message = self.getMessage(active_socket)
            print(message)
            if not (message):
                self.client_sockets.remove(active_socket)
                self.client_list = [member for member in self.client_list if (member.socket != active_socket)]

            print(f'received {message["type"]}')

    def monitorRoom(self):
        """
        goes though list of socket connections and creates a thread for each
        :return:
        """
        print("running room")
        while True:
            if self.client_sockets == []:
                self.client_sockets.append(self.socket_server)
            #select.select takes in a read, wite and error list. no write list and anyhting in read list could be an error. timeout 0
            r_sockets, w_sockets, ex_sockets = select.select(self.client_sockets, [], self.client_sockets, 0)

            for active_socket in r_sockets:
                threading.Thread(target=self.clientReceiver, args=active_socket)


def run():
    chatroom = Room(1)
    threading.Thread(target=chatroom.portListen, args=()).start()
    threading.Thread(target=chatroom.monitorRoom, args=()).start()





run()



