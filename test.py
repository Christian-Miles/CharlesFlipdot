import network
import time
from machine import UART, Pin

def byte_to_ascii(number):
    hex_str = hex(int(number))[2:]
    hex_str = '0' + hex_str if len(hex_str) == 1 else hex_str
    return [ord(x) for x in hex_str.upper()]

def write_to_display(address, resolution, to_be_sent, uart):
    res_hanover_format = byte_to_ascii(resolution)
    header = ['\x02', '\x31', '\x53', byte_to_ascii(address)[1], res_hanover_format[0], res_hanover_format[1]]
    footer = '\x03\x00\x00'
    data = ''
    packet = f'{''.join(str(x) for x in header)}{data}{footer}'
    uart.write(packet)

# Definitions
UART = machine.UART(1, baudrate=9600)
ADDRESS = 5
ROWS = 7
COLUMNS = 56

# Dynamically allocated
RES = ROWS*COLUMNS / 8

write_to_display(5, RES, '', UART)