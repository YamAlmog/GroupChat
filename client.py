import socket
import logging
import argparse
import threading
from error import InvalidNameException

END_CHAT = 'exit'
HEADER=1024

logging.basicConfig(filename='app.log', filemode='w',  level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def send_message(socket):
    while True:
        msg_to_send = input('')
        try:    
            socket.send(msg_to_send.encode())
        except socket.error as e:
            raise OSError(f"Error with sending data:{e}")
        if msg_to_send.lower() == END_CHAT:
            print("Closing the chat...")
            socket.close()
            break


def receive_message(socket):   
    while True: 
        try: 
            friend_msg = socket.recv(HEADER).decode('utf-8')
        except socket.error as e:
            raise OSError(f"Error with receiving data:{e}")
        print(friend_msg)            
 

def start(socket):
    try:    
        server_message = socket.recv(HEADER).decode('utf-8')
    except socket.error as e:
            raise OSError(f"Error with receiving data:{e}")
 
    name = input(f'{server_message}:\n')
    if name == '':
        socket.close()
        raise InvalidNameException("You must enter your name, empty value does not accepted.")
    try:
        socket.send(name.encode())
    except socket.error as e:
            raise OSError(f"Error with sending data:{e}")
    
    print('To exit the chat, type the word: EXIT')
    
    sender_thread = threading.Thread(target=send_message, args=(socket,))
    receiver_thread = threading.Thread(target=receive_message, args=(socket,))

    sender_thread.start()
    receiver_thread.start()

    sender_thread.join()  
    receiver_thread.join()




def main():
    try:    
        parser = argparse.ArgumentParser(description='This program implements a chat between users')
        parser.add_argument('SERVER_IP', type=str, help='The server IP to connect with')
        parser.add_argument('PORT', type=int, help='The port number to listen on')
        args = parser.parse_args()
        
        SERVER_IP = args.SERVER_IP
        PORT = args.PORT

        my_socket = socket.socket()
        my_socket.connect((SERVER_IP, PORT))

        logging.debug("client is connecting\n")
        logging.debug("waiting for the server to response\n")
        start(my_socket)
        
    except InvalidNameException as ex:
        print(f"Error: {ex}")
    except OSError as ex:
        print(f"Error: {ex}")    
    except argparse.ArgumentError as ex:
        print(f"Error: {ex}")
    except Exception as ex:
        print(f"Error: {ex}")

if __name__ == "__main__":
    main()