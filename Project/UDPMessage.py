import struct
import binascii


def send_offer(port):
    magic_cookie = 0xfeedbeef
    message_type = 0x02
    arr = struct.pack('QQQ', magic_cookie, message_type, port)
#    print([access_bit(arr,i) for i in range(len(arr)*8)])
    return arr


def access_bit(data, num):
    base = int(num // 8)
    shift = int(num % 8)
    return (data[base] & (1<<shift)) >> shift