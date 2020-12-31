import struct

'''
There are two important functions here, {send_offer} for the server to send 
a UDP message to all clients with the specified format. and {unpack_offer}
for the client in order to receive the UDP message from the server with the 
specified format.
'''


def send_offer(port):
    magic_cookie = 0xfeedbeef
    message_type = 0x2
    arr = struct.pack('IBH', magic_cookie, message_type, port)
    return arr


def unpack_offer(udp_packet):
    # We shouldn't allow a case of getting a UDP message with wrong format.
    try:
        unpacked_data = struct.unpack('IBH', udp_packet)
        if unpacked_data[0] == 0xfeedbeef and unpacked_data[1] == 0x2:
            return unpacked_data[2]
        return None
    except struct.error as err:
        print("Error while unpacking UDP packet : "+str(err))
        return None
