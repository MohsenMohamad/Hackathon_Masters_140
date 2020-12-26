import socket
import threading
import UDPMessage
import time
import random


server_port = 2050  # initiate port no above 1024
broadcast_port = 13117  # this should be the port in the end when we test it
group1 = {}
group2 = {}
group1_result = 0
group2_result = 0
counter1_lock = threading.Lock()
counter2_lock = threading.Lock()
game_result = "\nGame over!\n"


def server_broadcast():

    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)   # broadcast socket
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    # Enable broadcasting mode
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server.settimeout(0.2)   # Set a timeout so the socket does not block indefinitely when trying to receive data.
    message = UDPMessage.send_offer(server_port)

    # server accept socket

    host = socket.gethostname() # get the hostname
    server_socket = socket.socket()  # get instance
    server_socket.bind((host, server_port))  # bind host address and port together
    server_socket.setblocking(False)    # set socket to non-blocking mode
    server_socket.listen()      # configure how many client the server can listen simultaneously

    while True:
        stop_broadcast = time.time() + 10
        while time.time() < stop_broadcast:
            server.sendto(message, ('<broadcast>', broadcast_port))
            try:
                conn, address = server_socket.accept()  # accept new connection
                team_name = conn.recv(1024).decode()  # add the team's name
                conn.setblocking(False)
                print("Connection from: " + str(address))
                if random.choice([1, 2]) == 1:
                    client_thread = threading.Thread(target=start_game, args=(conn,))
                    group1[team_name] = client_thread
                else:
                    client_thread = threading.Thread(target=start_game, args=(conn,))
                    group2[team_name] = client_thread

            except:
                print(end='\r')
            time.sleep(1)
    #    setup_teams()  # assign each team to randomly selected group
        for t in group1.values():
            t.start()
        for t in group2.values():
            t.start()

        time.sleep(10)
        print_result()
        group1.clear()
        group2.clear()


def start_game(connection_socket):

    connection_socket.send(start_game_msg().encode())
    end_game = time.time()+10
    while time.time() < end_game:
        try:
            # receive data stream. it won't accept data packet greater than 1024 bytes
            data = connection_socket.recv(1024).decode()
            if not data:
                # if data is not received break
                break
            if threading.current_thread() in group1.values():
                with counter1_lock:
                    global group1_result
                    group1_result += 1
            else:
                with counter2_lock:
                    global group2_result
                    group2_result += 1
        except:
            print(end='\r')
    connection_socket.send(game_result.encode())
    connection_socket.close()  # close the connection


def concatenate_list_data(lst):
    result = ""
    for element in lst:
        result += element
        result += "\n"
    return result


def start_game_msg():
    game_message = "\nWelcome to Keyboard Spamming Battle Royale.\nGroup 1:\n==\n"
    msg = game_message + concatenate_list_data(group1)
    msg += "Group 2:\n==\n"
    msg += concatenate_list_data(group2)
    msg += "Start pressing keys on your keyboard as fast as you can!!\n"
    return msg


def print_result():
    global group1_result
    global group2_result
    str1 = "Group 1 typed in " + str(group1_result) + " characters. "
    str2 = "Group 2 typed in " + str(group2_result) + " characters."
    print(game_result + str1 + str2)
    if group1_result > group2_result:
        winners = concatenate_list_data(group1) + "Game over, sending out offer requests..."
        print("\033[1;3;32mGroup 1 wins!\033[0m\n\nCongratulations to the winners:\n==\n" + winners)
    elif group2_result > group1_result:
        winners = concatenate_list_data(group2) + "Game over, sending out offer requests..."
        print("\033[1;3;32mGroup 2 wins!\033[0m\n\nCongratulations to the winners:\n==\n" + winners)
    else:
        print("\033[0;31mDraw!\033[0m\nNone of the groups won the game!\n" + "Game over, sending out offer requests...")
    group1_result = 0
    group2_result = 0


if __name__ == '__main__':
    print("Server started,listening on IP address : " + socket.gethostbyname(socket.gethostname()))
    server_broadcast()
