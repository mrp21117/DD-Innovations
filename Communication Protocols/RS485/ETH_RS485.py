import socket
import time

# Configuration
converter_ip = '192.168.1.200'  # IP address of your Ethernet to RS485 converter
converter_port = 4196           # Port number (Modbus TCP default port)

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

rs485_command = b'\x01\x02\x03\xE8\x00\x08'

high_byte, low_byte = calculate_crc16(rs485_command_read)

rs485_command_read += bytes([low_byte, high_byte])

sock.sendall(rs485_command_read)
print(f"Sent: {rs485_command_read}")

# Wait for the response
response = sock.recv(1024)
print(f"Received: {response}")
