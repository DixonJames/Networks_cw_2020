import socket
import threading
import sys


header_size = 30



type_display = ['TO-ALL:', 'WHISPER:', 'CHANGE NAME REQUEST:', "REQUEST TO QUIT", "REQUEST LIST OF USERS", "BROADCAST TO EVERYONE", "REQUESTED LIST OF COMMANDS", "ANNOUNCEMENT"]

command_prefixes = ['/all', '/whisper', '/newname', '/quit', '/users', '/broadcast', '/help']
type_lookup = {'/all':0, '/whisper':1, '/newname':2, '/quit':3, '/users':4, '/broadcast':5, '/help':6}



#exeption classes to deal with errors
class Server_err(Exception):
    pass
class IncorrectArguments(Exception):
    pass



def rev_dict_lookup(dict, seach_val):
    """
    reverses the key and value lookup for a dictionary
    :param dict: dic being used
    :param seach_val: value to find key of
    :return: key value
    """
    for record in dict.items():
        key, val = record
        if val == seach_val:
            return key
    return False

def constuctMessage(message, type, sender):
    """
    :param message: msg content
    :param type: message type
    :param sender: entity sendinf the message
    :return: puts message header and message content together with correct white spacing and order
    """
    msg = f'{len(message):<10}' + f'{type:<10}' + f'{sender:<10}' + message
    return (msg).encode()


def receiveMessage(socket):
    """
    takes in header and then rest of message dynamicaly depending on header contents
    :param socket: socket to receive message from
    :return: deconstructed message and header data
    """
    sum_message = ''
    fresh = True
    take_in = header_size

    try:
        while True:
            part = (socket.recv(take_in)).decode()
            if fresh:
                take_in = int(part[0:9])
                message_type = part[10:19]
                sender = part[20:]
                fresh = False
            else:
                sum_message += part

            if len(sum_message) >= take_in:
                return message_type, sender, sum_message

    except:
        pass

def display_message(message, type):
    """
    displays the input message on the terminal in a human understandable format
    """
    message = f"{type_display[int(type)]} : {message}"
    print(message)
    print(">>")



def input_message():
    """
    takes command or message in from user
    also validates if entered commands are valid
    :return: currently formatted and encoded message with a header
    """

    user_in = str(input('>>'))
    if user_in == "":
        return False
    if user_in[0] == '/':
        command = (user_in.split(' '))[0]

        if command in command_prefixes:
            command_code = type_lookup[command]

            return constuctMessage(user_in[(len(command)+1):], command_code, username)
        else:
            print("INVALID COMMAND")
            return False
    else:
        return constuctMessage(user_in, 0, username)

def send_message(recipients, msg = None):
    """
    sends the msg to each recipient in the recipients list
    """
    if msg == None:
        msg = input_message()
        if msg == False:
            return False
    for recipient in recipients:
        recipient.send(msg)








def continuousSending():
    """
    will send messages until there is no longer a connection to the server
    :return:
    """
    while True:
        try:
            send_message([send_socket])
        except:
            print('server closed')
            exit(1)

def continuousReceiving():
    """
    continuously takes in and displayed messages sent to it
    :return:
    """
    while True:
        try:

            message_type, sender, message = receiveMessage(send_socket)
            display_message(message, message_type, sender)
        except:
            continue


def valid_username(username):
    """
    validates weather a username is valid (no spaces)
    user will be prompted to enter again untill it is valid
    :param username: username to check
    :return:
    """
    while(" " in username):
        username = str(input(">please enter a username without a space>"))[0:9]
    return username


def validate_arguments():
    if len(sys.argv) != 4:
        raise IncorrectArguments(f"program called with {len(sys.argv)} arguments. Should be max of 2")

    else:
        username = str(sys.argv[1])[0:9]
        hostname = str(sys.argv[2])

        try:
            port = int(sys.argv[3])
        except Exception as e:
            raise Server_err(f"port specified ({sys.argv[3]}) is not an integer ") from e

        server = (hostname, port)

    return server, username

if __name__ == '__main__':
    """
    ckecking command line argumn
    """

    server, username = validate_arguments()

    #tries to connect to user specified server
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        send_socket.connect(server)
    except Exception as e:
        raise Server_err(f"could not connect to {server}") from e


    #validating useraname
    username = valid_username(username)
    #sending server the new useranme
    username_msg = constuctMessage(username, 0, username)
    send_socket.send(username_msg)

    #setting up and starting sending and receiving threads
    thread_sending = threading.Thread(target= continuousSending)
    thread_receiving = threading.Thread(target=continuousReceiving)

    thread_sending.start()
    thread_receiving.start()

    thread_sending.join()
    thread_receiving.join()











