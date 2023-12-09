import socket
import logging
import threading
import sys

HEADER=1024
PORT= 8020
SERVER_IP= 'localhost'
BIND=(SERVER_IP,PORT)
END_CHAT = 'exit'
server=socket.socket()
server.bind(BIND)

logging.basicConfig(stream=sys.stdout, filemode='w',  level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

lock = threading.Lock()
users_tuple_list =[]
threads_list = []
# -----------------handle_client func------------------------------------------
def handle_client(current_client: socket, current_client_name: str):
    global users_tuple_list
    while True:
        try:
            message = current_client.recv(HEADER).decode('utf-8')
        except socket.error as e:
            raise OSError(f"Error with receiving data:{e}")
        logging.info(f"{current_client_name} sent: {message}")

        lock.acquire()
        for client_tuple in users_tuple_list:
            client = client_tuple[0]

            if client != current_client:     
                if message.lower() == END_CHAT:
                    sentence = f"{current_client_name} left the chat"
                    try:
                        client.send(sentence.encode('utf-8'))
                    except socket.error as e:
                        raise OSError(f"Error with sending data:{e}")
                    logging.info(sentence)      
                    current_client.close()

                    users_tuple_list = [tup for tup in users_tuple_list if tup[0] != current_client]
                    
                else:    
                    try:    
                        client.send(f"{current_client_name}: {message}".encode('utf-8'))                     
                    except socket.error as e:
                        raise OSError(f"Error with sending data:{e}")
        lock.release()


def create_users_threads(server):
    
    global users_tuple_list
    global threads_list
    while True:
        try:    
            (user_socket, address) = server.accept()
        except socket.error as e:
                raise OSError(f"Connection error: {e}")
        logging.info(f"User connected")
        server_msg = "Entre name:"
        try:    
            user_socket.send(server_msg.encode('utf-8'))
        except socket.error as e:
            raise OSError(f"Error with sending data:{e}")
        try:
            user_name = user_socket.recv(HEADER).decode('utf-8')
        except socket.error as e:
            raise OSError(f"Error with receiving data:{e}")
        if user_name == '':
            continue
        logging.info(f"User name: {user_name}")
        user_tuple = (user_socket, user_name)
        users_tuple_list.append(user_tuple)

        user_handler_thread = threading.Thread(target=handle_client, args=(user_socket, user_name))
        logging.info('this is thread')
        user_handler_thread.start()
        threads_list.append(user_handler_thread)
    

# -------------------------------------------- Start func --------------------------------------------
def start(server):
    try:   
        global users_tuple_list
        global threads_list
        
        user_creator_thread = threading.Thread(target=create_users_threads, args=(server,))
        user_creator_thread.start()
        user_creator_thread.join()
        logging.debug(users_tuple_list)
        for thread in threads_list:       
            thread.join()
        
    except OSError as ex:
        raise OSError(f"Socket error: {ex}")
    except Exception as ex:
        raise Exception(f"Unknown error: {ex}")


def main():
    try:    
        server.listen()
        logging.debug(f"Server is listening on...")
        start(server)  
    except OSError as ex:
        print(ex)
    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    main()