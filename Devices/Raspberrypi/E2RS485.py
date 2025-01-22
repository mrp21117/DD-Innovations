import socket
import time

# Configuration
converter_ip = '192.168.1.200'  # IP address of your Ethernet to RS485 converter
converter_port = 4196            # Port number (Modbus TCP default port)

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to the converter
    sock.connect((converter_ip, converter_port))
    print(f"Connected to {converter_ip} on port {converter_port}")

    # Example command to send (Modbus RTU frame or custom protocol)
    #rs485_command = b'\x01\x03\x00\x00\x00\x10\x44\x06'  # Replace with your command
    #rs485_command = b'\x01\x02\x03\xE8\x00\x08\xF9\xBC'  #Read Digtal Inputs
    #rs485_command = b'\x01\x0F\x0B\xB8\x00\x08\x01\xFF\x1F\xB5'  #Turn On ALL Digtal Outputs
    rs485_command = b'\x01\x0F\x0B\xB8\x00\x08\x01\x80\x5E\x55'  #Turn Off ALL Digtal Outputs
    # Send the command
    sock.sendall(rs485_command)
    print(f"Sent: {rs485_command}")

    # Wait for the response
    response = sock.recv(1024)
    print(f"Received: {response}")

finally:
    # Close the socket
    sock.close()
    print("Connection closed")

