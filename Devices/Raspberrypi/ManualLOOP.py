import socket
import time

# Configuration
converter_ip = '192.168.1.200'  # IP address of your Ethernet to RS485 converter
converter_port = 4196            # Port number (Modbus TCP default port)

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#CRC Calculator
def calculate_crc16(data):
    crc = 0xFFFF
    for pos in data:
        crc ^= pos
        for _ in range(8):
            if (crc & 1) != 0:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    high_byte = (crc & 0xFF00) >> 8
    low_byte = crc & 0x00FF
    return high_byte, low_byte

#Separate Individual Inputs
def get_inputs_state(response):
    # Assuming the response contains input states in the format of a single byte
    input_states = response[3]  # Change the index based on actual Modbus RTU response structure
    states = [(input_states >> i) & 1 for i in range(8)]
    return states

#Operate Individual Coils
def set_outputs_state(coil_states):
    byte_value = 0
    for i, state in enumerate(coil_states):
        if state:
            byte_value |= (1 << i)
    return byte_value

try:
    # Connect to the converter
    sock.connect((converter_ip, converter_port))
    print(f"Connected to {converter_ip} on port {converter_port}")
    coil_states = [False,False,False,False,False,False,False,False]
    
    while(1):
        Add = int(input("Enter Address Value :"))
        Rly = int(input("Enter State Value : "))
        
        for step in range(8):
         #   coil_states = []
            for i in range(3000,3008,1):
                if i == Add and coil_state[step]:
                    if Rly == 1 :
                        coil_states[step].replace(True)
                    else:
                        coil_states[step].replace(False)

        byte_value = set_outputs_state(coil_states)
        
        # Example command to turn on/off individual digital outputs (Modbus RTU frame or custom protocol)
        rs485_command_write = b'\x01\x0F\x0B\xB8\x00\x08\x01' + byte_value.to_bytes(1, byteorder='big')
        high_byte, low_byte = calculate_crc16(rs485_command_write)
        rs485_command_write += bytes([low_byte, high_byte])
        sock.sendall(rs485_command_write)
        print(f"Sent: {rs485_command_write}")

        # Wait for the response
        response = sock.recv(1024)
        print(f"Received: {response}")
        print(coil_states)
            
except:
    # Close the socket
    sock.close()
    print("Connection closed")
