import socket
import threading
import UDPMessage
import time
import random
import Match
import ClientHandler
import ANSIColors

match = Match.Match()


def server_broadcast(server_port, broadcast_port):
    global match
    broadcast_socket = create_broadcast_socket()
    message = UDPMessage.send_offer(server_port)
    server_socket = create_server_socket(server_port)

    while True:
        match = Match.Match()
        stop_broadcast = time.time() + 10
        while time.time() < stop_broadcast:
            broadcast_socket.sendto(message, ('<broadcast>', broadcast_port))
            try:
                conn, address = server_socket.accept()  # accept new connection
                conn.setblocking(True)
                team_name = conn.recv(1024).decode()  # add the team's name
                handler = ClientHandler.ClientHandler(conn, match)
                client_thread = threading.Thread(target=handler.start_game)
                print("Connection from: " + str(address))
                if random.choice([1, 2]) == 1:
                    match.add_team_to_group1(team_name, client_thread)
                else:
                    match.add_team_to_group2(team_name, client_thread)
            except:
                print(end='\r')
            time.sleep(1)
        match.run_client_threads()
        match.join_client_threads()
        match.print_result()


def create_broadcast_socket():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)   # broadcast socket
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    # Enable broadcasting mode
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    udp_socket.settimeout(0.2)   # Set a timeout so the socket does not block indefinitely when trying to receive data.
    return udp_socket


def create_server_socket(server_port):
    host = socket.gethostname()  # get the hostname
    server_socket = socket.socket()  # get instance
    server_socket.bind((host, server_port))  # bind host address and port together
    server_socket.setblocking(False)  # set socket to non-blocking mode
    server_socket.listen()  # configure how many client the server can listen simultaneously
    return server_socket


if __name__ == '__main__':
    ANSIColors.turn_on_colors()
    serverPort = 2050  # initiate port no above 1024
    broadcastPort = 13117  # this should be the port in the end when we test it
    print("Server started,listening on IP address : " + socket.gethostbyname(socket.gethostname()))
    server_broadcast(serverPort, broadcastPort)