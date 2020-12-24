import socket
import threading


def server_program():

    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(8)
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
    print("Server started,listening on IP address : "+socket.gethostbyname(socket.gethostname()))
    server_program()