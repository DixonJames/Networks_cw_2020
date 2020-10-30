import socket, select

local_ip = '127.0.0.1'
port = 2222
Header_size = 20
type_display = ['TO-ALL:', 'TO-YOU:', 'COMMAND:']

def rev_dict_lookup(dict, seach_val):
    for key, val in dict:
        if val == seach_val:
            return val
    return False

def constuctMessage(message, type):
    return (f'{len(message):<10}' + f'{type:<10}' + message).encode()

def receiveMessage(socket):
    chunck_size = Header_size
    sum_parts = ''
    fresh = True
    try:
        while True:
            part = (socket.recv(chunck_size)).decode()
            if len(part) != 0:
                if fresh:
                    message_size = int(part[0:9])
                    message_type = part[10:19]
                    chunck_size = message_size
                    fresh = False
                else:
                    sum_parts += part

                if not(len(sum_parts) != message_size):
                    return message_type, sum_parts
            else:
                return False
    except:
        return False

def send_message(recipients, msg, type, sender):
    msg = sender + ':' + msg
    for recipient in recipients:
        recipient.send(constuctMessage(msg, type))




class room():
    def __init__(self, send_socket):
        self.all_socket_list = [send_socket]
        self.client_directory = {}
        self.client_username = {}

    def monitorRoom(self, room_socket):
        while True:
            r_sockets, w_sockets, e_sockets = select.select(self.all_socket_list, [], self.all_socket_list)

            for current_socket in r_sockets:
                if current_socket == room_socket:

                    #accepts the new connection reqest
                    cli_socket, cli_addr = current_socket.accept()

                    #brings in the message form the initial request
                    message_type, message_data = receiveMessage(room_socket)


                    self.all_socket_list.append(cli_socket)
                    self.client_directory[cli_socket] = cli_addr
                    self.client_username[cli_addr] = message_data

                    print(f"new connection from: {cli_addr}")

                else:
                    msg_type, msg = receiveMessage(current_socket)
                    if msg and msg_type is False:
                        print(f"user {self.client_username[self.client_directory[current_socket]]} disconnected")

                        self.all_socket_list.remove(current_socket)
                        del self.client_username[self.client_directory[current_socket]]
                        del self.client_directory[current_socket]

                print(f"message from:{self.client_username[self.client_directory[current_socket]]}:{type_display[int(msg_type)]}::{msg}")
                recipients = [recipient for recipient in r_sockets if not room_socket]
                if type == 1:
                    recipients = rev_dict_lookup(self.client_username, msg.split(' ')[0])





send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#allows to reconnect^
send_socket.bind((local_ip, 3333))

send_socket.listen()




while True:
    cli_sock, cli_addr = send_socket.accept()
    print(f'new member from {cli_addr}')
    cli_sock.send((constuctMessage("hello there", 1)).encode())


