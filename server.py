import socket, select

local_ip = '127.0.0.1'
port = 2222
header_size = 30
type_lookup = {'all': 0, 'whisper':1, 'command':2, 'USERNAME':3}
type_display = ['TO-ALL:', 'TO-YOU:', 'COMMAND:', "username now:"]

def rev_dict_lookup(dict, seach_val):
    for key, val in dict:
        if val == seach_val:
            return val
    return False

def constuctMessage(message, type, sender):
    return (f'{len(message):<10}' + f'{type:<10}' + f'{sender:<10}' + message).encode()

def receiveMessage(socket):
    sum_message = ''
    fresh = True
    take_in = header_size
    try:
        while True:
            part = (socket.recv(take_in)).decode()
            if fresh:
                take_in = int(part[0:9])
                message_type = int(part[10:19])
                sender = part[20:]
                fresh = False
            else:
                sum_message += part

            if not(len(sum_message) < take_in):
                if len(sum_message) != take_in:
                    print("oversized message received")
                    return False
                return message_type, sender, sum_message

    except:
        return False

def send_message(recipients, msg, type, sender):
    msg = sender + ':' + msg
    for recipient in recipients:
        recipient.send(constuctMessage(msg, type, sender))




class room():
    def __init__(self, port):
        self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listen_socket.bind((local_ip, port))

        self.listen_socket.listen()

        self.room_socket = self.listen_socket

        self.all_socket_list = [self.listen_socket]

        self.client_username = {}

    def monitorRoom(self):
        while True:
            r_sockets, w_sockets, e_sockets = select.select(self.all_socket_list, [], self.all_socket_list,1)


            for current_socket in r_sockets:
                if current_socket == self.room_socket:

                    #accepts the new connection reqest
                    cli_socket, cli_addr = current_socket.accept()
                    current_socket = cli_socket
                    #brings in the message form the initial request
                    try:
                        message_type,message_sender, message_data = receiveMessage(cli_socket)
                        self.client_username[cli_socket] = message_data

                        self.all_socket_list.append(cli_socket)

                        print(f"new connection from {message_data} @ {cli_addr}")
                    except:
                        print(f"error receiving message from: {cli_socket}")




                else:
                    message_type,message_sender, message_data = receiveMessage(current_socket)
                    if message_data and message_type is False:
                        print(f"user {self.client_username[self.client_username[current_socket]]} disconnected")

                        self.all_socket_list.remove(current_socket)
                        del self.client_username[current_socket]

                        continue

                    print(f"USER:{self.client_username[current_socket]}:{type_display[int(message_type)]}::  {message_data}")

                recipients = [recipient for recipient in r_sockets if not self.room_socket or current_socket]

                if message_type == 0:
                    recipients = [recipient for recipient in r_sockets if not self.room_socket or current_socket]
                    send_message(recipients, message_data, message_type, message_sender)
                elif message_type == 1:
                    recipients = [recipient for recipient in r_sockets if recipient == message_data.split(" ")[0]]
                    send_message(recipients, message_data, message_type, message_sender)
                elif message_type == 2:
                    #code commands in later
                    print(f"command {message_data} issues by {message_sender}")
                    continue
                else:
                    continue

                send_message(recipients, message_data, message_type, message_sender)








room1 = room(port)
room1.monitorRoom()


"""
while True:
    cli_sock, cli_addr = send_socket.accept()
    print(f'new member from {cli_addr}')
    cli_sock.send((constuctMessage("hello there", 1)).encode())
"""

