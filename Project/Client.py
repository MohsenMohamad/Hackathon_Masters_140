import socket
import UDPMessage
import threading
import KeyListen
import ANSI
# Constant variables
TEAM_NAME = "Masters\n"
BUFF_SIZE = 1024
MAX_TIMEOUT = 10


def client_listen(broadcast_port):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # create UDP socket
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Enable broadcasting mode
    client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    client.bind(("", broadcast_port))   # bind the socket to the broadcast port to receive invitations
    while True:
        data, addr = client.recvfrom(BUFF_SIZE)     # listen for game invitations from servers' broadcasts
        invitation_port = UDPMessage.unpack_offer(data)     # socket server port number
        if invitation_port is None:     # the message is corrupt or is not formatted right
            continue
        host_name = addr[0]     # get the invitation sender's ip
        msg = ANSI.get_cyan() + "Received offer from " + ANSI.get_end()+ANSI.get_yellow()+str(host_name)+ANSI.get_end()
        msg += (ANSI.get_cyan() + ", attempting to connect..." + ANSI.get_end())
        print(msg)
        client_connect(host_name, invitation_port)      # Attempt to establish a connection with the server to play
        clear_previous_invitations(client)      # so we do not try to connect using old invitations
        print(ANSI.get_cyan() + "\nServer disconnected, listening for offer requests..." + ANSI.get_end())


def client_connect(hostname, port):

    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.settimeout(MAX_TIMEOUT)
    try:
        tcp_socket.connect((hostname, port))  # connect to the server
    except socket.error as err:
        print(ANSI.get_red() + "Error while trying to connect to server : "+str(err) + ANSI.get_end())
        return
    try:
        tcp_socket.sendall(TEAM_NAME.encode())      # send the team name to the server
    except socket.error as err:
        print(ANSI.get_red() + "Error at sending the team name : "+str(err) + ANSI.get_red())
        tcp_socket.close()
        return
    tcp_socket.settimeout(socket.getdefaulttimeout())
    client_game(tcp_socket)     # the client is ready for the game


def client_game(conn_socket):
    stop_keyboard_event = threading.Event()     # this will be a pill to kill the keyboard thread
    keyboard_thread = threading.Thread(target=listen, args=(conn_socket, stop_keyboard_event,))
    try:
        welcome_message = conn_socket.recv(BUFF_SIZE).decode()      # receive welcome message from the server
        clear_input_buffer()        # make sure that we will not count any chars from the buffer if there is any
        print(welcome_message)
        keyboard_thread.start()     # start the thread whose job is to count keyboard hits
        while True:
            data = conn_socket.recv(BUFF_SIZE).decode()  # receive messages from the server
            if not data:
                break
            print(data)  # print the messages received from the server
        stop_keyboard_event.set()   # terminate the keyboard listener thread because the game is over
        conn_socket.close()  # close the connection
    except socket.error as err:
        print(ANSI.get_red() + "Error during the game : "+str(err) + ANSI.get_end())
        stop_keyboard_event.set()   # terminate the keyboard listener thread because there has been a connection error
        conn_socket.close()
        return


def clear_previous_invitations(client):  # cleaning the buffers out
    client.setblocking(False)   # make the socket non-blocking so we can receive from it without blocking
    while True:
        try:
            client.recv(BUFF_SIZE)      # read from the buffer until there is no more data and and exception is thrown
        except socket.error:
            client.setblocking(True)    # no more data in the buf , change the socket to blocking mode before returning
            return


def listen(conn_socket, stop_keyboard):  # Keyboard listener for the clients match
    buffer_listener = KeyListen.KBHit()
    while not stop_keyboard.wait(0):    # loop until the main client thread terminates the listener thread
        if buffer_listener.kbhit():     # if a key has been hit , do this :
            buffered_char = buffer_listener.getch()     # fetch the key and try to send it to the server
            try:
                conn_socket.sendall(str(buffered_char).encode())  # encode and send the key
            except socket.error as err:
                print(ANSI.get_red() + "Could not send the keyboard input to server : " + str(err) + ANSI.get_end())


def clear_input_buffer():
    while KeyListen.KBHit().kbhit():
        KeyListen.KBHit().getch()   # pop a char from the input buffer until it is empty


if __name__ == '__main__':
    ANSI.turn_on_colors()   # enable virtual terminal in windows application to support ANSI coloring
    broadcastPort = 13117
    print(ANSI.get_cyan() + "Client started, listening for offer requests..." + ANSI.get_end())
    client_listen(broadcastPort)    # start the client
