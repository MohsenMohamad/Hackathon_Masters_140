import socket
import threading
import UDPMessage
import time
import random
import Match
import ClientHandler

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
        time.sleep(10)
        match.print_result()
    #    group1.clear()
    #    group2.clear()


if __name__ == '__main__':
    serverPort = 2050  # initiate port no above 1024
    broadcastPort = 13117  # this should be the port in the end when we test it
    print("Server started,listening on IP address : " + socket.gethostbyname(socket.gethostname()))
    server_broadcast(serverPort, broadcastPort)
