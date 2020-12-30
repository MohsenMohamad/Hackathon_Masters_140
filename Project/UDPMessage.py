import struct


def send_offer(port):
    magic_cookie = 0xfeedbeef
    message_type = 0x02
    arr = struct.pack('>IBH', magic_cookie, message_type, port)
    return arr


def unpack_offer(udp_packet):
    unpacked_data = struct.unpack('>IBH', udp_packet)
    return unpacked_data[2]


def access_bit(data, num):
    base = int(num // 8)
    shift = int(num % 8)
    return (data[base] & (1 << shift)) >> shift
