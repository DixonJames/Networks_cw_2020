import socket


server = ("127.0.0.1", 2222)
listen = ("127.0.0.1", 7777)

header_size = 30

type_lookup = {'/all':0, '/whisper':1, '/newname':2, '/quit':3, '/users':4}

type_display = ['TO-ALL:', 'TO-YOU:', 'COMMAND:', "username now:"]
command_prefixes = ['/all', '/whisper', '/newname', '/quit', '/users']

log = []
username = "Iam Afiller"

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
                message_type = part[10:19]
                sender = part[20:]
                fresh = False
            else:
                sum_message += part

            if len(sum_message) >= take_in:
                return message_type, sender, sum_message



    except:
        return False, False, False

def display_message(message, type, sender):
        message = f"{sender}|{type} : {message}"
        log.append(message)
        print(message)



def input_message():

    user_in = str(input('>>'))
    if user_in == "":
        return False
    if user_in[0] == '/':
        command = (user_in.split(' '))[0]

        if command in command_prefixes:
            command_code = type_lookup[command]
            return constuctMessage(user_in[(len(command)+2):], command_code, username)
        else:
            print("INVALID COMMAND")
            return False
    else:
        return constuctMessage(user_in, 0, username)

def send_message(recipients, msg = None):
    if msg == None:
        msg = input_message()
        if msg == False:
            return False
    for recipient in recipients:
        recipient.send(msg)




recv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
recv_socket.bind(listen)



if __name__ == '__main__':
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    send_socket.connect(server)
    #send_socket.setblocking(False)

    #listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #listen_socket.bind(listen)

    #listen_socket.listen()




    username = str(input(">useranme>"))

    username_msg = constuctMessage(username, 0, username)
    send_socket.send(username_msg)

    while True:

        #need to get these two bits running in paralell
        try:
            send_message([send_socket])
        except:
            print('server closed')
            exit(1)

        try:

            message_type, sender, message = receiveMessage(send_socket)
            display_message(message, message_type, sender)
        except:
            continue











