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
                team_name = receive_team_name(conn, stop_broadcast-time.time())  # add the team's name
                if team_name is None:
                    conn.close()
                else:
                    handler = ClientHandler.ClientHandler(conn, team_name, match)
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
        threading.current_thread()
        match.join_client_threads()
        if match.is_valid():
            print(ANSI.get_cyan() + "\nGame over, sending out offer requests...\n" + ANSI.get_end())
    #    match.print_result()


def create_broadcast_socket():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)   # broadcast socket
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    # Enable broadcasting mode
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    return udp_socket


def create_server_socket(server_port):
    host = socket.gethostname()  # get the hostname
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  # get instance
    server_socket.bind((host, server_port))  # bind host address and port together
    server_socket.setblocking(False)  # set socket to non-blocking mode
    server_socket.listen()  # configure how many client the server can listen simultaneously
    return server_socket


def receive_team_name(client_socket, timeout):
    start_time = time.time()
    client_socket.settimeout(timeout)
    while True:
        if time.time()-start_time > timeout:
            print(ANSI.get_red() + "Could not get the team name in time" + ANSI.get_end())
            return None
        try:
            team_name = str(client_socket.recv(1024), 'utf-8')
            if not team_name:
                print(ANSI.get_red() + "Client socket closed" + ANSI.get_end())   # print its ip maybe ?
                return None
            if team_name[len(team_name)-1] == '\n':
                clear_socket_input_buffer(client_socket)    # if the team name contains \n
                break
            else:
                client_socket.close()
                return None
        except socket.error as err:
            print(ANSI.get_red() + "Error while receiving the team name : "+str(err) + ANSI.get_end())
            return None
    return team_name[:len(team_name)-1]


def clear_socket_input_buffer(client_socket):
    client_socket.setblocking(False)
    while True:
        try:
            client_socket.recv(1024)
        except socket.error:
            client_socket.setblocking(True)
            break


if __name__ == '__main__':
    ANSI.turn_on_colors()
    serverPort = 2050  # initiate port no above 1024
    broadcastPort = 13117  # this should be the port in the end when we test it
    msg = ANSI.get_cyan() + "Server started,listening on IP address : " + ANSI.get_end()
    msg += (ANSI.get_yellow() + socket.gethostbyname(socket.gethostname()) + ANSI.get_end())
    print(msg)
    server_broadcast(serverPort, broadcastPort)
