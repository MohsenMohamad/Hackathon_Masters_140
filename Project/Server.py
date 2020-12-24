import socket
import threading
import UDPMessage
import time


def server_broadcast():

    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Enable broadcasting mode
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    # Set a timeout so the socket does not block
    # indefinitely when trying to receive data.
    server.settimeout(0.2)
    message = UDPMessage.send_offer(5000)

    while True:
        port_number = 13117  # this should be the port in the end when we test it
        port_number = 5000
        server.sendto(message, ('<broadcast>', port_number))
#        print("announcement sent!")
        time.sleep(1)


def server_accepting():
    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(4)

    while True:
        conn, address = server_socket.accept()  # accept new connection
        print("Connection from: " + str(address))
        client_thread = threading.Thread(target=start_game, args=(conn,))
        client_thread.start()


def start_game(connection_socket):
    counter = 0
    while True:
        print(counter)
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = connection_socket.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        print(data)
        counter = counter + 1
        connection_socket.send(str(counter).encode())  # send data to the client

    connection_socket.close()  # close the connection


if __name__ == '__main__':
    UDPMessage.send_offer(50)
    print("Server started,listening on IP address : " + socket.gethostbyname(socket.gethostname()))
    broadcast_thread = threading.Thread(target=server_broadcast)
    broadcast_thread.start()
    server_accepting()