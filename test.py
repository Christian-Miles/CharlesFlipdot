import time
from machine import UART, Pin


def byte_to_ascii(number):
    hex_str = hex(int(number))[2:]
    hex_str = '0' + hex_str if len(hex_str) == 1 else hex_str
    return ''.join([x for x in hex_str.upper()])

def checksum(header, packet):
    sumval = sum([int(ord(x)) for x in header]) + sum([int(ord(x)) for x in packet]) & 0xFF
    crc = (sumval ^ 255) + 1
    return byte_to_ascii(crc)

def write_to_display(address, resolution, to_be_sent, uart):
    res_hanover_format = byte_to_ascii(resolution)
    header = ''.join(['\x02', '\x31', '\x53', byte_to_ascii(address)[1], res_hanover_format])
    footer = '\x03' # \x03 + checksum bytes (2)
    packets_to_send = 56

    ## Just a test for now
    to_be_sent = [0,0,0,255,8,8,8,255]
    to_be_sent.extend([0]*(packets_to_send-len(to_be_sent)))
    data = ''.join([byte_to_ascii(x) for x in to_be_sent])

    footer += checksum(header, data)

    packet = f'{header}{data}{footer}'
    uart.write(packet)

# Definitions
uart = machine.UART(1, baudrate=9600)
ADDRESS = 5
ROWS = 7
COLUMNS = 56

# Dynamically allocated
RES = ROWS*COLUMNS / 8

write_to_display(5, RES, '', uart)