import socket
import logging
import argparse
import threading
END_CHAT = 'exit'
HEADER=1024

logging.basicConfig(filename='app.log', filemode='w',  level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def send_message(socket):
    try:    
        while True:
            msg_to_send = input('')
            socket.send(msg_to_send.encode())
            if msg_to_send.lower() == END_CHAT:
                print("Closing the chat...")
                break
    except OSError:
        raise OSError("Socket error occurred")
    except Exception:
        raise Exception("Unknown error occurred")
    finally:
        socket.close()

def receive_message(socket, friend_name):
    try:    
        while True: 
            
            friend_msg = socket.recv(HEADER).decode('utf-8')
            print(f"{friend_name}: {friend_msg}")
            
            if friend_msg.lower() == END_CHAT:
                print("Closing the chat...")
                socket.close()
                break      
    except OSError:
        raise OSError("Socket error occurred")
    except Exception:
        raise Exception("Unknown error occurred")




def start(socket):
    try:    
        server_message = socket.recv(HEADER).decode('utf-8')

        if server_message == "Entre name:":
            name = input('Enter your name:\n')
            socket.send(name.encode())
            print('To exit the chat, type the word: EXIT')
            friend_name = socket.recv(HEADER).decode('utf-8')
            sender_thread = threading.Thread(target=send_message, args=(socket,))
            receiver_thread = threading.Thread(target=receive_message, args=(socket, friend_name))

            sender_thread.start()
            receiver_thread.start()

            sender_thread.join()  
            receiver_thread.join()
        
        else:
            print('There was an error with the server, try next time.')
            socket.close()
            
    except OSError as ex:
        raise OSError(ex)
    except Exception as ex:
        raise Exception(ex)
    


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
    
    except argparse.ArgumentError as ex:
        print(f"Error: {ex}")
    except Exception as ex:
        print(f"Error: {ex}")

if __name__ == "__main__":
    main()