import socket
import threading
import UDPMessage
import time
import random
import Match
import ClientHandler
import ANSI


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
                handler = ClientHandler.ClientHandler(conn, match)
                team_name = handler.receive_team_name(stop_broadcast-time.time())  # add the team's name
                if team_name is None:
                    conn.close()
                else:
                    client_thread = threading.Thread(target=handler.start_game)
                    print(ANSI.get_cyan() + "Connection from: " + str(address) + ANSI.get_end())
                    if random.choice([1, 2]) == 1:
                        match.add_team_to_group1(team_name, client_thread)
                    else:
                        match.add_team_to_group2(team_name, client_thread)
            except socket.error:    # for timeout exceptions since we call accept from a non-blocking socket
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
    ANSI.turn_on_colors()
    serverPort = 2050  # initiate port no above 1024
    broadcastPort = 13117  # this should be the port in the end when we test it
    msg = ANSI.get_cyan() + "Server started,listening on IP address : " + ANSI.get_end()
    msg += (ANSI.get_yellow() + socket.gethostbyname(socket.gethostname()) + ANSI.get_end())
    print(msg)
    server_broadcast(serverPort, broadcastPort)
