import socket
import threading

server = ("127.0.0.1", 2222)
listen = ("127.0.0.1", 7777)

header_size = 30



type_display = ['TO-ALL:', 'TO-YOU:', 'COMMAND:', "username now:"]
command_prefixes = ['/all', '/whisper', '/newname', '/quit', '/users']

type_lookup = {'/all':0, '/whisper':1, '/newname':2, '/quit':3, '/users':4, '/broadcast':5}



log = []
username = "Iam Afiller"

def rev_dict_lookup(dict, seach_val):
    for key, val in dict:
        if val == seach_val:
            return val
    return False

def constuctMessage(message, type, sender):
    msg = f'{len(message):<10}' + f'{type:<10}' + f'{sender:<10}' + message
    return (msg).encode()


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
        pass

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

            return constuctMessage(user_in[(len(command)+1):], command_code, username)
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








def continuousSending():
    while True:

        #need to get these two bits running in paralell
        try:
            send_message([send_socket])
        except:
            print('server closed')
            exit(1)

def continuousReceiving():
    while True:
        try:

            message_type, sender, message = receiveMessage(send_socket)
            display_message(message, message_type, sender)
        except:
            continue


if __name__ == '__main__':
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    send_socket.connect(server)

    username = str(input(">useranme>"))

    username_msg = constuctMessage(username, 0, username)
    send_socket.send(username_msg)


    thread_sending = threading.Thread(target= continuousSending)
    thread_receiving = threading.Thread(target=continuousReceiving)

    thread_sending.start()
    thread_receiving.start()

    thread_sending.join()
    thread_receiving.join()











