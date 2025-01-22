import serial
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.exceptions import ModbusException

# Configuration parameters
PORT = "COM3"  # Replace with your COM port (e.g., "COM3" on Windows, "/dev/ttyUSB0" on Linux)
BAUDRATE = 9600
STOPBITS = 1
BYTESIZE = 8
PARITY = 'N'  # None ('N'), Even ('E'), Odd ('O')

SLAVE_ID = 1  # Modbus device ID
REGISTER_ADDRESS = 0x0000  # Replace with the Modbus register address
REGISTER_COUNT = 1  # Number of registers to read/write

def main():
    # Initialize Modbus serial client
    client = ModbusClient(
        method='rtu',
        port=PORT,
        baudrate=BAUDRATE,
        stopbits=STOPBITS,
        bytesize=BYTESIZE,
        parity=PARITY,
        timeout=1  # Timeout in seconds
    )

    # Connect to the Modbus device
    if not client.connect():
        print("Failed to connect to Modbus device.")
        return

    try:
        # Read Holding Registers
        response = client.read_holding_registers(
            address=REGISTER_ADDRESS,
            count=REGISTER_COUNT,
            unit=SLAVE_ID
        )
        if response.isError():
            print(f"Error reading register: {response}")
        else:
            print(f"Register values: {response.registers}")

        # Write to a Holding Register (example)
        write_value = 123  # Replace with the value you want to write
        write_response = client.write_register(
            address=REGISTER_ADDRESS,
            value=write_value,
            unit=SLAVE_ID
        )
        if write_response.isError():
            print(f"Error writing to register: {write_response}")
        else:
            print(f"Successfully wrote value {write_value} to register {REGISTER_ADDRESS}")

    except ModbusException as e:
        print(f"Modbus error: {e}")
    finally:
        # Close the connection
        client.close()
        print("Connection closed.")

if __name__ == "__main__":
    main()
