import socket

local_ip = '127.0.0.1'
port = 2223
header_size = 10
type_lookup = {'all': 0, 'whisper':1, 'command':2}
type_display = ['TO-ALL:', 'TO-YOU:', 'COMMAND:']
log = []

send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
send_socket.bind((local_ip, 2222))

def constuctMessage(message, type):
    return (f'{len(message):<10}' + f'{type:<10}' + message).encode()


def receiveMessage(socket):
    sum_message = ''
    fresh = True

    while True:
        part = (socket.recv(20)).decode()
        if fresh:
            message_size = int(part[0:9])
            message_type = part[10:19]
            fresh = False
        else:
            sum_message += part

        if not(len(sum_message) != message_size):
            return message_type, sum_message

def display_message(message, type):
        message = message.split(' ')[0] + '::' + type_display[type] + message.split(' ')[1:]
        log.append(message)
        print(message)



def input_message():

    user_in = str(input('>>'))
    if user_in[0] == '/':
        command = (user_in.split(' '))[0][1:]
        try:
            command_code = type_lookup[command]
            return constuctMessage(user_in[(len(command)+2):], command_code)
        except:
            return False
    else:
        return constuctMessage(user_in, 0)

while True:
    print(input_message())



'''
send_socket.connect((local_ip, 3334))

type, message = receiveMessage(send_socket)
print(message,type )
'''







