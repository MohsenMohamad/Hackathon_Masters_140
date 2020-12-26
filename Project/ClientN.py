import asyncio
import struct
import socket
from pynput.keyboard import Listener


broadcast_port = 13117
team_name = "Instinct"
reader = 0
writer = 0


async def client_listen():

    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Enable broadcasting mode
    client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    client.bind(("", broadcast_port))
    while True:
        data, addr = client.recvfrom(1024)
        unpacked_data = struct.unpack('QQQ', data)
        host_name = addr[0]  # (eth1, 172.1.0/24) is for development , (eth2, 172.99.0/24) is to test your work
        print("Received offer from " + str(host_name) + ", attempting to connect...")
        invitation_port = unpacked_data[2]    # socket server port number
        await client_connect(host_name, invitation_port)


async def client_connect(hostname, port):
    global reader, writer
    reader, writer = await asyncio.open_connection(hostname, port)  # connect to the server
    writer.write(team_name.encode())
    with Listener(on_release=on_release) as listener:
        await client_game()


async def client_game():

    #   the server should send a tcp packet to stop the game at the end
    while True:
        data1 = await reader.read(1024)
        data = data1.decode()  # receive response
        if not data:
            break
    #    print('Counter : ' + data)  # show in terminal
        print(data)  # show in terminal
    writer.close()  # close the connection
    print("Server disconnected, listening for offer requests...")


async def on_release(key):
    writer.write(str(key).encode())    # send message


if __name__ == '__main__':
    asyncio.run(client_listen())
    # asyncio.run(tcp_echo_client('Hello World!'))
