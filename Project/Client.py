import socket
from pynput.keyboard import Key, Listener
import threading
import UDPMessage
import struct


tcp_socket = socket.socket()
team_name = "Instinc\nt"


def client_listen(broadcast_port):

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
        print("\nServer disconnected, listening for offer requests...")


def client_connect(hostname, port):

    tcp_socket.settimeout(10)
    try:
        tcp_socket.connect((hostname, port))  # connect to the server
    except socket.error as err:
        print("Error while trying to connect to server : "+str(err))
        return

    try:
        tcp_socket.sendall((team_name + "\n").encode())
    except socket.error as err:
        print("Error at sending the team name : "+str(err))
        tcp_socket.close()
        return
    tcp_socket.settimeout(socket.getdefaulttimeout())
    client_game()


def client_game():
    try:
        welcome_message = tcp_socket.recv(1024).decode()
        print(welcome_message)
        with Listener(on_release=on_release) as listener:
            #   the server should send a tcp packet to stop the game at the end
            while True:
                data = tcp_socket.recv(1024).decode()  # receive response
                if not data:
                    break
                print(data)  # show in terminal
            tcp_socket.close()  # close the connection
    except socket.error as err:
        print("Error during the game : "+str(err))
        tcp_socket.close()
        return


def on_release(key):
    try:
        tcp_socket.sendall(str(key).encode())    # send message
    except socket.error as err:
        print("Could not send the keyboard input to server : "+str(err))


def clear_previous_invitations(client):
    client.setblocking(False)
    while True:
        try:
            client.recv(1024)
        except socket.error:
            client.setblocking(True)
            return


if __name__ == '__main__':
    broadcastPort = 13117
    print("Client started, listening for offer requests...")
    client_listen(broadcastPort)



