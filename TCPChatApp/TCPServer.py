'''
The code used is from https://www.youtube.com/watch?v=CV7_stUWvBQ
'''

import socket
import select

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234

'''Set up a TCP socket that uses IPv4 addressing, set the socket option,
bind the socket to the defined IP and PORT variables, and make the
server constantly listen for new connections, i.e. participants in a chat
room.'''
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP, PORT))
server_socket.listen()

#Collects the sockets that are created in the application.
sockets_list = [server_socket]

#A dictionary of connected clients with socket as the key, pointing to
#the usernames
clients = {}

print(f'Listening for connections on {IP}:{PORT}...')
#Decides what to do when it revieves or doesn't recieve a message from a user.
def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)
        #If no data is recieved, the client closes the connection
        if not len(message_header):
            return False
        #Convert header to int value
        message_length = int(message_header.decode('utf-8').strip())
        #Return an object of message header and message data
        return {'header': message_header, 'data': client_socket.recv(message_length)}
    #Occurs when client interrupts programs and closes it
    except:
        return False

while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
    #Iterate over notified sockets
    for notified_socket in read_sockets:
        #Accept a new connection
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()
            user = receive_message(client_socket)
            if user is False:
                continue
            sockets_list.append(client_socket)
            clients[client_socket] = user
            print('Accepted new connection from {}:{}, username: {}'.format(*client_address, user['data'].decode('utf-8')))
        #An existing socket is sending a message
        else:
            message = receive_message(notified_socket)
            #If message is false, the client disconnects, therefore they are
            #removed from the sockets_list and list of clients.
            if message is False:
                print('Closed connection from: {}'.format(clients[notified_socket]['data'].decode('utf-8')))
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue
            #Get specific user information and print out both name and message.
            user = clients[notified_socket]
            print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')
            #Send message to every other member of the chat except the sender
            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
