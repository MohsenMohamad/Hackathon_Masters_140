import socket
import Match
import time
import threading


class ClientHandler:

    def __init__(self, connection_socket, match):
        self.client_socket = connection_socket
        self.match = match

    def start_game(self):
        time_out = 10
        self.client_socket.settimeout(time_out)
        end_game = time.time() + 10
        self.client_socket.sendall(self.match.start_game_msg().encode())
        while time.time() < end_game:
            try:
                time_out = end_game - time.time()
                if time_out < 0:
                    time_out = 0
                self.client_socket.settimeout(time_out)
                # receive data stream. it won't accept data packet greater than 1024 bytes
                data = self.client_socket.recv(1024).decode()
                if not data:
                    # if data is not received break
                    break
                if threading.current_thread() in self.match.group1.values():
                    self.match.inc_g1_counter()
                else:
                    self.match.inc_g2_counter()
            except socket.error as err:
                print(err)
                self.client_socket.close()  # close the connection
                return
        self.client_socket.close()  # close the connection
