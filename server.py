import socket
import logging
import threading

HEADER=1024
PORT= 8020
SERVER_IP= 'localhost'
BIND=(SERVER_IP,PORT)
END_CHAT = 'exit'
server=socket.socket()
server.bind(BIND)

logging.basicConfig(filename='app.log', filemode='w',  level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

lock = threading.Lock()

# -----------------handle_client func------------------------------------------
def handle_client(server, current_client, other_client, current_client_name):
    try:
        while True:
            message = current_client.recv(HEADER).decode('utf-8')
            other_client.send(message.encode('utf-8'))

            logging.info(f"{current_client_name} sent: {message}")

            if message.lower() == END_CHAT:
                logging.info('The conversation is over.')
                break
            else:
                continue
    except OSError as ex:
        raise OSError(f"Socket error: {ex}")
    finally:
        current_client.close()
        other_client.close()
        server.close() 




# -------------------------------------------- Start func --------------------------------------------
def start(server):
    try:   
        (user_1, address_1) = server.accept()
        logging.info("User 1 connected")
        (user_2, address_2) = server.accept()
        logging.info("User 2 connected")

        server_msg = "Entre name:"
        user_1.send(f'{server_msg}'.encode('utf-8'))
        user_2.send(f'{server_msg}'.encode('utf-8'))

        name_1 = user_1.recv(HEADER).decode('utf-8')
        logging.info(f"User 1 name: {name_1}")

        name_2 = user_2.recv(HEADER).decode('utf-8')
        logging.info(f"User 2 name: {name_2}")

        user_1.send(name_2.encode('utf-8'))
        user_2.send(name_1.encode('utf-8'))

        user1_handler_thread = threading.Thread(target=handle_client, args=(server, user_1, user_2, name_1))
        user2_handler_thread = threading.Thread(target=handle_client, args=(server, user_2, user_1, name_2))

        user1_handler_thread.start()
        user2_handler_thread.start()

        user1_handler_thread.join()  
        user2_handler_thread.join()
        
    except OSError as ex:
        raise OSError(f"Socket error: {ex}")


def main():
    try:    
        server.listen()
        logging.info(f"Server is listening on...")
        start(server)
    except OSError as ex:
        print(f"Error: {ex}")



if __name__ == "__main__":
    main()