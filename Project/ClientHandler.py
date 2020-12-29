import socket
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

        try:
            self.client_socket.sendall(self.match.start_game_msg().encode())
        except socket.error as err:
            print("Error while sending welcome message to team "+str(err))
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
                print(err)
                self.client_socket.close()  # close the connection
                return
        self.client_socket.close()  # close the connection

    def receive_team_name(self, timeout):
        start_time = time.time()
        self.client_socket.settimeout(timeout)
        team_name = ""
        while True:
            if time.time()-start_time > timeout:
                print("Could not get the team name in time")
                return None
            try:
                char = self.client_socket.recv(1).decode()
                if not char:
                    print("Client socket closed")   # print its ip maybe ?
                    return None
                if char == "\n":
                    self.clear_socket_input_buffer()    # if the team name contains \n
                    break
                team_name += char
            except socket.error as err:
                print("Error while receiving the team name : "+str(err))
                return None
        return team_name

    def clear_socket_input_buffer(self):
        self.client_socket.setblocking(False)
        while True:
            try:
                self.client_socket.recv(1024)
            except socket.error:
                self.client_socket.setblocking(True)
                break
