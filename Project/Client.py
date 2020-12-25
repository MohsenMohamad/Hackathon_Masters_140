import socket
from pynput.keyboard import Key, Listener
import threading
import UDPMessage
import struct


tcp_socket = socket.socket()
broadcast_port = 13117
team_name = "Instinct"


def client_listen():

    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDPygyggygyygygygygygygygygygyg
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Enable broadcasting mode
    client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    client.bind(("", broadcast_port))
    while True:
        global tcp_socket
        tcp_socket = socket.socket()
        data, addr = client.recvfrom(1024)
        unpacked_data = struct.unpack('QQQ', data)
#       print(hex(unpacked_data[0]))
        host_name = addr[0]  # (eth1, 172.1.0/24) is for development , (eth2, 172.99.0/24) is to test your work
        print("Received offer from " + str(host_name) + ", attempting to connect...")
        invitation_port = unpacked_data[2]    # socket server port number
        client_connect(host_name, invitation_port)


def client_connect(hostname, port):

    print(port)
    tcp_socket.connect((hostname, port))  # connect to the server
    tcp_socket.send((team_name + "\n").encode())
    with Listener(on_release=on_release) as listener:
        client_game()


def client_game():

    #   the server should send a tcp packet to stop the game at the end
    while True:
        data = tcp_socket.recv(1024).decode()  # receive response
        if not data:
            break
    #    print('Counter : ' + data)  # show in terminal
        print(data)  # show in terminal
    tcp_socket.close()  # close the connection
    print("Server disconnected, listening for offer requests...")


def on_release(key):
    tcp_socket.send(str(key).encode())    # send message


if __name__ == '__main__':
    print("Client started, listening for offer requests...")
    client_listen()



