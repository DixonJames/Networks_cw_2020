import socket, select
import sys
import logging
logging.basicConfig(filename='server.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

local_ip = '127.0.0.1'
port = 2222


header_size = 30
type_lookup = {'/all':0, '/whisper':1, '/newname':2, '/quit':3, '/users':4, '/broadcast':5, 'help':6}

type_display = ['TO-ALL:', 'WHISPER:', 'CHANGE NAME REQUEST:', "REQUEST TO QUIT", "REQUEST LIST OF USERS", "BROADCAST TO EVERYONE", "REQUESTED LIST OF COMMANDS", "ANNOUNCEMENT"]
command_prefixes = ['/all', '/whisper', '/newname', '/quit', '/users', '/broadcast', '/help']

command_description = ['sends to all OTHER users (selected by default if no \'/\' entered)', 'sends to one user '
                                                                                             'specified user',
                       'changes users username to a new one of users choice', 'asks server to remove user\'s socket '
                                                                              'from the list on the server. also '
                                                                              'closes the users client program',
                       'send a list of all current users usernames to users client', 'sends message to ALL clients '
                                                                                     'currently connected to server', 'displays all command and their descriptions (this!)']

command_templates = ['/all -message here-', '/whisper -username- -message-', '/newname -username to chang to-', '/quit', '/users', '/broadcast -message-', '/help' ]


#exeption classes to deal with errors
class Server_err(Exception):
    pass
class UserDisconnectErr(Exception):
    pass
class UnknownProtocolErr(Exception):
    pass
class IncorrectArguments(Exception):
    pass


def helpString():
    """
    constructs the help string to be sent to the user
    """
    whole = ''

    for c in range(len(command_prefixes)):

        whole += '\n'+ 'command: ' + command_prefixes[c]
        whole += '\n' +'template: '+ command_templates[c]
        whole += '\n' + 'description: ' + command_description[c]
        whole += '\n'
    return whole

def rev_dict_lookup(dict, seach_val):
    """
    does a reverse dict lookup
    """
    for record in dict.items():
        key, val = record
        if val == seach_val:
            return key
    return None

def constuctMessage(message, type, sender):
    """
    :param message: msg content
    :param type: message type
    :param sender: entity sendinf the message
    :return: puts message header and message content together with correct white spacing and order
    """
    return (f'{len(message):<10}' + f'{type:<10}' + f'{sender:<10}' + message).encode()

def receiveMessage(socket):
    """
    takes in header and then rest of message dynamicaly depending on header contents
    :param socket: socket to receive message from
    :return: deconstructed message and header data
    """
    sum_message = ''
    fresh = True
    take_in = header_size


    while True:
        try:
            part = (socket.recv(take_in)).decode()
            if part == '' and fresh:
                return False, False, False
        except:
            logging.error(f"error receiving message from {socket}")
            return False, False, False

        if fresh:
            take_in = int(part[0:9])
            message_type = int(part[10:19])
            sender = part[20:]
            fresh = False
        else:
            sum_message += part

        if not(len(sum_message) < take_in):
            if len(sum_message) != take_in:
                raise UnknownProtocolErr("oversized Msg received")
            return message_type, sender, sum_message

def send_message(recipients, msg, type, sender, sender_socket):
    """
    sends the msg to each recipient in the recipients list
    """
    msg = str(sender) + ': ' + str(msg)
    for recipient in recipients:
        try:
            recipient.sendall(constuctMessage(msg, type, sender))
        except Exception as e:
            print(f'error sending to {recipient}')
            #raise Server_err(f'error sending to {recipient}') from e

class room():

    def __init__(self, port):
        self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listen_socket.bind((local_ip, port))
        self.listen_socket.listen()


        self.room_socket = self.listen_socket

        self.all_socket_list = [self.listen_socket]

        self.client_username = {}

        self.client_return_addr = {}



    def recipientsViaType(self, message_type, all_posible_recipients,sender, message_data=None ):
        """
        works out who should receive the message based off the type of message and who sent it
        :return: list of users sockets
        """



        # to all
        if message_type == 5 or message_type == 2 or message_type == 3 :
            return all_posible_recipients

        # to one whisperUser
        if message_type == 1:
            if sender:
                #reverse dict lookup

                all_posible_recipients = [rev_dict_lookup(self.client_username, message_data.split(" ")[0])]
                if all_posible_recipients != [None]:
                    return all_posible_recipients
                return None



        if message_type == 4:
            return [sender]

        if message_type == 0 or message_type == 7:
            return [r for r in all_posible_recipients if r != sender]

    def commandHandler(self, All_posibles_recipients, sender_socket, whole_msg, message_type):
        """
            depending on the message type (ie what command being requested) will perfrom command specifics here
            :return:
        """
        try:
            arguments = whole_msg.split(" ")
        except Exception as e:
            print(f"error receiving message from: {sender_socket}")
            pass


        # if mesage not a command, sends to the recipients. handles messages to all and recipients
        if message_type == 0 :
            send_message(All_posibles_recipients, whole_msg, 0, self.client_username[sender_socket], self.room_socket)

        elif message_type == 5 :
            send_message(All_posibles_recipients, whole_msg, 5, self.client_username[sender_socket], self.room_socket)

        #whisper
        elif message_type == 1 :
            if All_posibles_recipients == None:
                send_message([sender_socket], 'no user by this name', 0, 'server', self.room_socket)
            else:
                send_message(All_posibles_recipients, whole_msg.split(' ', 1)[1], 1, self.client_username[sender_socket], self.room_socket)



        # change nickname to first arg, inform everyone
        elif message_type == 2:
            newname = ''
            fresh = True
            for part in arguments:
                if fresh:
                    newname += str(part)
                else:
                    newname += ' ' + str(part)
                fresh = False

            if newname == '':
                msg = 'must enter a valid name'
            elif newname not in self.client_username.values():
                newname = newname[0:min(len(newname), 9)]
                msg = f"User {self.client_username[sender_socket]} is now {newname}"
                self.client_username[sender_socket] = newname


            else:
                msg = f"Username {newname} is already taken"

            send_message(All_posibles_recipients, msg, 0, 'SERVER', self.room_socket)

        #client does a controlled quit. all other users notified and client removed from all server lists
        elif message_type == 3:
            msg = f"user {self.client_username[sender_socket]} disconnected"

            self.all_socket_list.remove(sender_socket)
            del self.client_username[sender_socket]

            send_message(All_posibles_recipients, msg, 0, 'SERVER', self.room_socket)

        elif message_type == 7:
            msg = f"{self.client_username[sender_socket]} has joined"

            send_message(All_posibles_recipients, msg, 0, 'SERVER', self.room_socket)

        #sends list of current users to client
        elif message_type == 4:
            send_message([sender_socket], list(self.client_username.values()), 0, 'SERVER', self.room_socket)

        elif message_type == 6:
            send_message([sender_socket], helpString(), 6, 'SERVER', self.room_socket)

    def monitorRoom(self):
        """
        the infinite loop that constantly goes through the list of sockets
        checks for new users to add to sockets list
        checks for disconnected users
        checks if current users have sent a new message
        """
        while True:
            r_sockets, w_sockets, e_sockets = select.select(self.all_socket_list, [], self.all_socket_list,1)


            for current_socket in r_sockets:
                if current_socket == self.room_socket:
                    disconnect = False

                    #accepts the new connection reqest
                    cli_socket, cli_addr = current_socket.accept()
                    current_socket = cli_socket

                    #brings in the message form the initial request
                    try:
                        message_type,message_sender, message_data = receiveMessage(cli_socket)

                        self.client_username[cli_socket] = message_data
                        self.all_socket_list.append(cli_socket)
                        self.client_return_addr[cli_socket] = message_sender

                        #send_message([cli_socket], f'WELCOME to the server {message_data}', 0, "server", self.room_socket)


                        print(f"new connection from {message_data} @ {cli_addr}")


                        logging.info(f"new connection from {message_data} @ {cli_addr}")

                        message = f"welcome to the server {message_data}"
                        message_sender = self.room_socket
                        message_type = 5
                        send_message([cli_socket], message, 5, 'SERVER',self.room_socket)

                        message_data = f"{message_data} has joined"
                        message_type = 7



                    except Exception as e:


                        logging.error(f"error receiving connect message from: {cli_socket}")

                        error_msg = f"error receiving connect message from: {cli_socket}"
                        self.all_socket_list = []
                        self.client_username = []
                        raise Server_err(error_msg) from e


                else:
                    message_type,message_sender, message_data = receiveMessage(current_socket)

                    if (message_type,message_sender, message_data) == (False, False, False):
                        #messy disconnect
                        message_data = f"user {self.client_username[current_socket]} disconnected"
                        print(message_data)



                        logging.info(f"{message_data}")

                        message_type = 3
                        quiting_user = self.client_username[current_socket]

                        message_sender = self.room_socket

                        disconnect = True





                    #otherwise the received message is valid and gets printed to server screen

                    if not(disconnect):
                        print(f"{self.client_username[current_socket]}:{type_display[int(message_type)]}>  {message_data}")



                        logging.info(f"{self.client_username[current_socket]}:{type_display[int(message_type)]}>  {message_data}")



                #finds clients to send result of received msg to
                #message_type, all_posible_recipients,sender, message_data=None
                recipients = self.recipientsViaType(message_type, [recipient for recipient in self.all_socket_list if recipient != self.room_socket],current_socket, message_data)



                #logging.info(f"{type_display[message_type]} : {message_sender} : {message_data}")

                self.commandHandler(recipients, current_socket, message_data, message_type)
                disconnect = False





if __name__ == '__main__':
    if len(sys.argv) > 2:
        raise IncorrectArguments(f"program called with {len(sys.argv)} arguments. Should be max of 2 (server.py [port])")

    if len(sys.argv) > 1:
        port = int(sys.argv[1])

    chatroom = room(port)
    chatroom.monitorRoom()
