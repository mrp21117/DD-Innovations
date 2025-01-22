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

#Read Output Coils
def read_outputs():
    #command to read Coils (Modbus RTU frame or custom protocol)
    rs485_command_read = b'\x01\x01\x0B\xB8\x00\x08'  # Read Digital Inputs
    high_byte, low_byte = calculate_crc16(rs485_command_read)
    rs485_command_read += bytes([low_byte, high_byte])
    sock.sendall(rs485_command_read)
    print(f"Sent: {rs485_command_read}")

    # Wait for the response
    response = sock.recv(1024)
    print(f"Received: {response}")

    # Get individual input states
    output_states = get_inputs_state(response)
    print(f"Output States: {output_states}")
    
#write outputs coils
def write_outputs():
    Add = int(input("Enter Address Value (3000-3007): "))
    Rly = int(input("Enter State Value (0 or 1): "))

    if Add < 3000 or Add > 3007:
        print("Invalid address. Please enter a value between 3000 and 3007.")

    step = Add - 3000  # Map address to coil_states index

    coil_states[step] = True if Rly == 1 else False
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

# read digital inputs (Modbus RTU frame or custom protocol)
def read_inputs():
    rs485_command_read = b'\x01\x02\x03\xE8\x00\x08'  # Read Digital Inputs
    high_byte, low_byte = calculate_crc16(rs485_command_read)
    rs485_command_read += bytes([low_byte, high_byte])
    sock.sendall(rs485_command_read)
    print(f"Sent: {rs485_command_read}")

    # Wait for the response
    response = sock.recv(1024)
    print(f"Received: {response}")

    # Get individual input states
    input_states = get_inputs_state(response)
    print(f"Input States: {input_states}")


try:
    # Connect to the converter
    sock.connect((converter_ip, converter_port))
    print(f"Connected to {converter_ip} on port {converter_port}")
    coil_states = [False, False, False, False, False, False, False, False]
    
    print(" 1-(Read Inputs)\n 2-(Read Outputs)\n 3-(Write Outputs)\n 4- (Read Inputs and Outputs)")

    while True:
        f = int(input("Select the Function:")) 
        if f == 1 :
            read_inputs()
        elif f == 2 :
            read_outputs()
        elif f == 3 :
            write_outputs()
        elif f == 4 :
            print("Discrete Read Inputs")
            read_inputs()
            print()
            print("Read Output Relays")
            read_outputs()

            
except:
    # Close the socket
    sock.close()
    print("Connection closed")

