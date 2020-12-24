import socket
from pynput.keyboard import Key,Listener
import threading
import UDPMessage
import struct


tcp_socket = socket.socket()


def client_program():

    while True:
        data = tcp_socket.recv(1024).decode()  # receive response
        print('Counter : ' + data)  # show in terminal

    game_socket.close()  # close the connection


def on_release(key):
    tcp_socket.send(str(key).encode())    # send message


def client_listen():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Enable broadcasting mode
    client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    host_name = socket.gethostname()   #The dev network (eth1, 172.1.0/24) is used for development, and the test network (eth2, 172.99.0/24) will be used to test your work

    client.bind(("", 5000))
    while True:
        data, addr = client.recvfrom(1024)
        print("received message: %s" % data)
        print(hex(struct.unpack('QQQ', data)[0]))
#        print([UDPMessage.access_bit(data, i) for i in range(len(data) * 8)])
        invitation_port = struct.unpack('QQQ', data)[2]
    #    tcp_socket = socket.socket()  # instantiate
        tcp_socket.connect((host, port))  # connect to the server
    #    game_thread = threading.Thread(target=client_program())
    #    game_thread.start()

        with Listener(on_release=on_release) as listener:
            client_program()


if __name__ == '__main__':
    print("Client started, listening for offer requests...")
    client_listen()



