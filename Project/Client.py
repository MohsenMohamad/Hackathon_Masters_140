import socket
import UDPMessage
import threading
import KeyListen
import ANSI

team_name = "Masters\n"


def client_listen(broadcast_port):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Enable broadcasting mode
    client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    client.bind(("", broadcast_port))
    while True:
        data, addr = client.recvfrom(1024)
        invitation_port = UDPMessage.unpack_offer(data)     # socket server port number
        if invitation_port is not None:
            host_name = addr[0]  # (eth1, 172.1.0/24) is for development , (eth2, 172.99.0/24) is to test your work
            msg = ANSI.get_cyan() + "Received offer from " + ANSI.get_end()+ANSI.get_yellow()+str(host_name)+ANSI.get_end()
            msg += (ANSI.get_cyan() + ", attempting to connect..." + ANSI.get_end())
            print(msg)
            client_connect(host_name, invitation_port)
            clear_previous_invitations(client)
            print(ANSI.get_cyan() + "\nServer disconnected, listening for offer requests..." + ANSI.get_end())


def client_connect(hostname, port):

    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.settimeout(10)
    try:
        tcp_socket.connect((hostname, port))  # connect to the server
    except socket.error as err:
        print(ANSI.get_red() + "Error while trying to connect to server : "+str(err) + ANSI.get_end())
        return
    try:
        tcp_socket.sendall(team_name.encode())
    except socket.error as err:
        print(ANSI.get_red() + "Error at sending the team name : "+str(err) + ANSI.get_red())
        tcp_socket.close()
        return
    tcp_socket.settimeout(socket.getdefaulttimeout())
    client_game(tcp_socket)


def client_game(conn_socket):
    stop_keyboard_event = threading.Event()
    keyboard_thread = threading.Thread(target=listen, args=(conn_socket, stop_keyboard_event,))
    try:
        welcome_message = conn_socket.recv(1024).decode()
        clear_input_buffer()
        print(welcome_message)
        keyboard_thread.start()
        while True:
            data = conn_socket.recv(1024).decode()  # receive response
            if not data:
                break
            print(data)  # show in terminal
        stop_keyboard_event.set()
        conn_socket.close()  # close the connection
    except socket.error as err:
        print(ANSI.get_red() + "Error during the game : "+str(err) + ANSI.get_end())
        stop_keyboard_event.set()
        conn_socket.close()
        return


def clear_previous_invitations(client):  # cleaning the buffers out
    client.setblocking(False)
    while True:
        try:
            client.recv(1024)
        except socket.error:
            client.setblocking(True)
            return


def listen(conn_socket, stop_keyboard):  # Keyboard listener for the clients match
    buffer_listener = KeyListen.KBHit()
    while not stop_keyboard.wait(0):
        if buffer_listener.kbhit():
            buffered_char = buffer_listener.getch()
            try:
                conn_socket.sendall(str(buffered_char).encode())  # send message
            except socket.error as err:
                print(ANSI.get_red() + "Could not send the keyboard input to server : " + str(err) + ANSI.get_end())


def clear_input_buffer():
    while KeyListen.KBHit().kbhit():
        KeyListen.KBHit().getch()


if __name__ == '__main__':
    ANSI.turn_on_colors()
    broadcastPort = 13117
    print(ANSI.get_cyan() + "Client started, listening for offer requests..." + ANSI.get_end())
    client_listen(broadcastPort)
