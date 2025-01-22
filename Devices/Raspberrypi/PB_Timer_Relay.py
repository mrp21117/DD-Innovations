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

#Separate Individuals
def get_i_state(response):
    # Assuming the response contains input states in the format of a single byte
    input_states = response[3]  # Change the index based on actual Modbus RTU response structure
    states = [(input_states >> i) & 1 for i in range(8)]
    return states

#Operate Individual Coils
def set_i_state(coil_states):
    byte_value = 0
    for i, state in enumerate(coil_states):
        if state:
            byte_value |= (1 << i)
    return byte_value

# read digital inputs (Modbus RTU frame or custom protocol)
def read_inputs():
    rs485_command_read = b'\x01\x02\x03\xE8\x00\x08'  # Read Digital Inputs
    high_byte, low_byte = calculate_crc16(rs485_command_read)
    rs485_command_read += bytes([low_byte, high_byte])
    sock.sendall(rs485_command_read)
    # Wait for the response
    response = sock.recv(1024)
    return response

def read_outputs():
    #command to read Coils (Modbus RTU frame or custom protocol)
    rs485_command_read = b'\x01\x01\x0B\xB8\x00\x08'  # Read Digital Inputs
    high_byte, low_byte = calculate_crc16(rs485_command_read)
    rs485_command_read += bytes([low_byte, high_byte])
    sock.sendall(rs485_command_read)
    # Wait for the response
    response = sock.recv(1024)
    return response

def delay(n):
    time.sleep(n)

try:
    # Connect to the converter
    sock.connect((converter_ip, converter_port))
    print(f"Connected to {converter_ip} on port {converter_port}")
    
    while True:
        #Read Inputs
        PB = read_inputs()
        PB_List = get_i_state(PB)
        #print(f"Inputs:  {PB_List}")
        
        #Read Outputs
        Rly = read_outputs()
        Rly_List = get_i_state(Rly)
        #print(f"Outputs: {Rly_List}")
        
        k = False
        # Define variable to give individual output bits value for 8 coils
        coil_states = []
        for i in range(8):
            if PB_List[i] == 1 :
                time.sleep(3)
                if PB_List[i] == 1 :
                    coil_states.append(True)
                    k = True
            else:
                coil_states.append(False)
        byte_value = set_i_state(coil_states)
        
        #command to turn on/off individual outputs (Modbus RTU frame or custom protocol)
        rs485_command_write = b'\x01\x0F\x0B\xB8\x00\x08\x01' + byte_value.to_bytes(1, byteorder='big')
        high_byte, low_byte = calculate_crc16(rs485_command_write)
        rs485_command_write += bytes([low_byte, high_byte])
        sock.sendall(rs485_command_write)
        while(k):
            print(f"Inputs:  {PB_List}")
            print(coil_states)
            print()
            delay(5)
            break

        # Wait for the response
        response = sock.recv(1024)
        #print(coil_states)
        
        #Re Check Outputs
        Rly = read_outputs()
        Rly_List = get_i_state(Rly)
        #print(f"Outputs: {Rly_List}")
        
        #time.sleep(2)
        #break
            
except:
    # Close the socket
    sock.close()
    print("Connection closed")