import socket


server = ("127.0.0.1", 2222)
listen = ("127.0.0.1", 3333)

header_size = 30
type_lookup = {'all': 0, 'whisper':1, 'command':2, 'USERNAME':3}
type_display = ['TO-ALL:', 'TO-YOU:', 'COMMAND:', "username now:"]
log = []
username = "Iam Afiller"


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

            if not (len(sum_message) != take_in):
                return message_type, sender, sum_message

            else:
                return False
    except:
        return False

def display_message(message, type, sender):
        message = f"{sender}|{type} : {message}"
        log.append(message)
        print(message)



def input_message():

    user_in = str(input('>>'))
    if user_in == "":
        return False
    if user_in[0] == '/':
        command = (user_in.split(' '))[0][1:]
        try:
            command_code = type_lookup[command]
            return constuctMessage(user_in[(len(command)+2):], command_code, username)
        except:
            print("INVALID COMMAND")
            return False
    else:
        return constuctMessage(user_in, 0, username)

def send_message(recipients, msg = None):
    if msg == None:
        msg = input_message()
        if msg == False:
            return False
        print(msg)
    for recipient in recipients:
        recipient.send(msg)




recv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
recv_socket.bind(listen)



if __name__ == '__main__':
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(server)
    client_socket.setblocking(False)

    username = input(">useranme>")

    username_msg = constuctMessage(username, type_lookup['USERNAME'], username)
    client_socket.send(username_msg)

    while True:
        send_message([client_socket])
        try:
            message_type, sender, message = receiveMessage(client_socket)
            display_message(message, message_type, sender)
        except:
            continue



'''
send_socket.connect((local_ip, 3334))
fg
type, message = receiveMessage(send_socket)
print(message,type )
'''







