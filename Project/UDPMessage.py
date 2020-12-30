import struct


def send_offer(port):
    magic_cookie = 0xfeedbeef
    message_type = 0x2
    arr = struct.pack('IBH', magic_cookie, message_type, port)
    return arr


def unpack_offer(udp_packet):

    try:
        unpacked_data = struct.unpack('IBH', udp_packet)
        if unpacked_data[0] == 0xfeedbeef and unpacked_data[1] == 0x2:
            return unpacked_data[2]
        return None
    except struct.error as err:
        print("Error while unpacking UDP packet : "+str(err))
        return None


def access_bit(data, num):
    base = int(num // 8)
    shift = int(num % 8)
    return (data[base] & (1 << shift)) >> shift
