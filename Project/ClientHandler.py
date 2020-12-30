import socket
import time
import threading
import TeamStats
from ANSI import *


class ClientHandler:

    def __init__(self, connection_socket, team_name, match):
        self.client_socket = connection_socket
        self.team_name = team_name
        self.match = match

    def start_game(self):
        time_out = 10
        self.client_socket.settimeout(time_out)
        end_game = time.time() + 10

        try:
            self.client_socket.sendall(self.match.start_game_msg().encode())
        except socket.error as err:
            print(ANSI.RED + "Error while sending welcome message to team "+str(err) + ANSI.END)
            self.client_socket.close()
            return

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
                result_message = self.match.print_result()
                try:
                    self.client_socket.sendall(result_message.encode())
                except socket.error:
                    self.client_socket.close()
                print(end='\r')
                self.client_socket.close()  # close the connection
                return
        result_message = self.match.print_result()  # in case that the player types exactly with 0 secs left
        try:
            self.client_socket.sendall(result_message.encode())
        except socket.error:
            pass
        self.client_socket.close()  # close the connection
