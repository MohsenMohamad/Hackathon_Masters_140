import socket
import UDPMessage
import threading
import KeyListen

tcp_socket = socket.socket()
team_name = "Masters\n"
stop_keyboard = False


def client_listen(broadcast_port):
    global stop_keyboard
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Enable broadcasting mode
    client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    client.bind(("", broadcast_port))
    while True:
        global tcp_socket
        tcp_socket = socket.socket()
        data, addr = client.recvfrom(1024)
        invitation_port = UDPMessage.unpack_offer(data)     # socket server port number
        host_name = addr[0]  # (eth1, 172.1.0/24) is for development , (eth2, 172.99.0/24) is to test your work
        print("Received offer from " + str(host_name) + ", attempting to connect...")
        client_connect(host_name, invitation_port)
        clear_previous_invitations(client)
        stop_keyboard = False
        print("\nServer disconnected, listening for offer requests...")


def client_connect(hostname, port):

    tcp_socket.settimeout(10)
    try:
        tcp_socket.connect((hostname, port))  # connect to the server
    except socket.error as err:
        print("Error while trying to connect to server : "+str(err))
        return

    try:
        tcp_socket.sendall(team_name.encode())
    except socket.error as err:
        print("Error at sending the team name : "+str(err))
        tcp_socket.close()
        return
    tcp_socket.settimeout(socket.getdefaulttimeout())
    global stop_keyboard
    keyboard_thread = threading.Thread(target=listen)
    client_game(keyboard_thread)


def client_game(key_thread):
    global stop_keyboard
    try:
        welcome_message = tcp_socket.recv(1024).decode()
        print(welcome_message)
        key_thread.start()
        while True:
            data = tcp_socket.recv(1024).decode()  # receive response
            if not data:
                break
            print(data)  # show in terminal
        stop_keyboard = True
        tcp_socket.close()  # close the connection
    except socket.error as err:
        print("Error during the game : "+str(err))
        stop_keyboard = True
        tcp_socket.close()
        return


def clear_previous_invitations(client):
    client.setblocking(False)
    while True:
        try:
            client.recv(1024)
        except socket.error:
            client.setblocking(True)
            return


def listen():
    m = KeyListen.KBHit()
    while not stop_keyboard:
        if m.kbhit():
            k = m.getch()
            try:
                tcp_socket.sendall(str(k).encode())  # send message
            except socket.error as err:
                print("Could not send the keyboard input to server : " + str(err))


if __name__ == '__main__':
    broadcastPort = 13117
    print("Client started, listening for offer requests...")
    client_listen(broadcastPort)
