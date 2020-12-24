import socket
from pynput.keyboard import Key,Listener
import threading


host = socket.gethostname()  # as both code is running on same pc
port = 5000  # socket server port number
client_socket = socket.socket()  # instantiate
client_socket.connect((host, port))  # connect to the server



def client_program():

    while True:
        data = client_socket.recv(1024).decode()  # receive response
        print('Counter : ' + data)  # show in terminal

    client_socket.close()  # close the connection


def on_release(key):
    client_socket.send(str(key).encode())    # send message


if __name__ == '__main__':
    game_thread = threading.Thread(target=client_program)
    game_thread.start()
    with Listener(on_release=on_release) as listener:
        listener.join()
        game_thread.join()


