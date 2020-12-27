import socket
import threading
import UDPMessage
import time
import random
import Match

match = Match.Match()


def server_broadcast(server_port, broadcast_port):
    global match
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)   # broadcast socket
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    # Enable broadcasting mode
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server.settimeout(0.2)   # Set a timeout so the socket does not block indefinitely when trying to receive data.
    message = UDPMessage.send_offer(server_port)

    host = socket.gethostname()  # get the hostname
    server_socket = socket.socket()  # get instance
    server_socket.bind((host, server_port))  # bind host address and port together
    server_socket.setblocking(False)    # set socket to non-blocking mode
    server_socket.listen()      # configure how many client the server can listen simultaneously

    while True:
        match = Match.Match()
        stop_broadcast = time.time() + 10
        while time.time() < stop_broadcast:
            server.sendto(message, ('<broadcast>', broadcast_port))
            try:
                conn, address = server_socket.accept()  # accept new connection
                conn.setblocking(True)
                team_name = conn.recv(1024).decode()  # add the team's name
                client_thread = threading.Thread(target=start_game, args=(conn,))
                print("Connection from: " + str(address))
                if random.choice([1, 2]) == 1:
                    match.add_team_to_group1(team_name, client_thread)
                else:
                    match.add_team_to_group2(team_name, client_thread)

            except:
                print(end='\r')
            time.sleep(1)
        for t in match.group1.values():
            t.start()
        for t in match.group2.values():
            t.start()
        time.sleep(10)
        match.print_result()
    #    group1.clear()
    #    group2.clear()


def start_game(connection_socket):
    time_out = 10
    connection_socket.settimeout(time_out)
    end_game = time.time() + 10
    connection_socket.sendall(match.start_game_msg().encode())
    while time.time() < end_game:
        try:
            time_out = end_game - time.time()
            if time_out < 0:
                time_out = 0
            connection_socket.settimeout(time_out)
            # receive data stream. it won't accept data packet greater than 1024 bytes
            data = connection_socket.recv(1024).decode()
            if not data:
                # if data is not received break
                break
            if threading.current_thread() in match.group1.values():
                match.inc_g1_counter()
            else:
                match.inc_g2_counter()
        except socket.error as err:
            print(err)
            connection_socket.close()  # close the connection
            return
    connection_socket.close()  # close the connection


if __name__ == '__main__':
    serverPort = 2050  # initiate port no above 1024
    broadcastPort = 13117  # this should be the port in the end when we test it
    print("Server started,listening on IP address : " + socket.gethostbyname(socket.gethostname()))
    server_broadcast(serverPort, broadcastPort)
