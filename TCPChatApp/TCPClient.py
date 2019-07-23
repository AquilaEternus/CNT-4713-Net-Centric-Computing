'''
The code used is from https://www.youtube.com/watch?v=ytu2yV3Gn1I
'''

import socket
import select
import errno

HEADER_LENGTH = 10

#Define IP address, port, and obtain username from client
IP = "127.0.0.1"
PORT = 1234
my_username = input("Username: ")

#Create a TCP client socket that uses IPv4 addressing
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Connect the client socket to the IP of 127.0.0.1 and PORT 1234
client_socket.connect((IP, PORT))
client_socket.setblocking(False)

#Encode both username and header to utf-8 before sending it across the socket.
username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)

while True:
    message = input(f'{my_username} > ')
    #Send the message if it is not empty
    if message:
        #Encode both message and header to utf-8 before sending it across the socket.
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)
    try:
        #Loop over messages sent by other users and print them to the user.
        while True:
            #Receive our "header" containing username length, it's size is defined and constant
            username_header = client_socket.recv(HEADER_LENGTH)
            if not len(username_header):
                print('Connection closed by the server')
                sys.exit()
            # Decode user and message header into the data and print them out
            username_length = int(username_header.decode('utf-8').strip())
            username = client_socket.recv(username_length).decode('utf-8')
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')
            print(f'{username} > {message}')
    #Occurs when the user is not recieving any messages. If this happens,
    #continue the connection and ignore unless somehting else occurs.
    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()
        continue
    #General exception. Simply exit the program.
    except Exception as e:
        print('Reading error: '.format(str(e)))
        sys.exit()
