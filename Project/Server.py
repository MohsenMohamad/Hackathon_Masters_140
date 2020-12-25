import socket
import threading
import UDPMessage
import time


server_port = 2050  # initiate port no above 1024
broadcast_port = 13117  # this should be the port in the end when we test it
teams = []  # do not forget to clear it after every match
game_result = "\ngame result"
synchro_object = threading.Condition()


def server_broadcast():

    # broadcast socket

    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Enable broadcasting mode
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    # Set a timeout so the socket does not block
    # indefinitely when trying to receive data.
    server.settimeout(0.2)
    message = UDPMessage.send_offer(server_port)

    # server accept socket

    # get the hostname
    host = socket.gethostname()

    server_socket = socket.socket()  # get instance

    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, server_port))  # bind host address and port together
    server_socket.setblocking(False)

    # configure how many client the server can listen simultaneously
    server_socket.listen()

    while True:
        stop_broadcast = time.time() + 10
        while time.time() < stop_broadcast:
            server.sendto(message, ('<broadcast>', broadcast_port))
            try:
                conn, address = server_socket.accept()  # accept new connection
                teams.append(conn.recv(1024).decode())  # add the team's name
                print("Connection from: " + str(address))
                client_thread = threading.Thread(target=start_game, args=(conn,))
                client_thread.start()
            except:
                print(end='\r')
            time.sleep(1)
        with synchro_object:
            synchro_object.wait()
        teams.clear()


def server_accepting():
    # get the hostname
    host = socket.gethostname()

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, server_port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen()

    while True:
        conn, address = server_socket.accept()  # accept new connection
        print(server_socket.getsockname())
        print(conn.getsockname())
        teams.append(conn.recv(1024).decode())  # add the team's name
        print(teams)
        print("Connection from: " + str(address))
        client_thread = threading.Thread(target=start_game, args=(conn,))
        client_thread.start()


def start_game(connection_socket):
    counter = 0
    end_game = time.time()+10
    connection_socket.setblocking(False)
    while time.time() < end_game:
        try:
            # receive data stream. it won't accept data packet greater than 1024 bytes
            data = connection_socket.recv(1024).decode()
            if not data:
                # if data is not received break
                break
            print(data)
            counter = counter + 1
            print(counter)
        #    connection_socket.send(str(counter).encode())  # send data to the client
        except:
            print(end='\r')
    connection_socket.send(game_result.encode())
    connection_socket.close()  # close the connection
    with synchro_object:
        synchro_object.notifyAll()


if __name__ == '__main__':
    print("Server started,listening on IP address : " + socket.gethostbyname(socket.gethostname()))
    server_broadcast()
#    broadcast_thread = threading.Thread(target=server_broadcast)
#    broadcast_thread.start()
#    server_accepting()
