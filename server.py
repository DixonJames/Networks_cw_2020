import socket

local_ip = '127.0.0.1'
port = 2222

def constuctMessage(message, type):
    return f'{len(message):<10}' + f'{type:<10}' + message

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


send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
send_socket.bind((local_ip, 3333))

receive_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
receive_socket.bind((local_ip, 3334))

receive_socket.listen(5)

while True:
    cli_sock, cli_addr = receive_socket.accept()
    print(f'new member from {cli_addr}')
    cli_sock.send((constuctMessage("hello there", 1)).encode())


