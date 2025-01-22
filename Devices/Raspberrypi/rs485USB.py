from pymodbus.client.sync import ModbusSerialClient as ModbuClient
from pymodbus.register_read_message import ReadInputRegisterResponse
client = ModbusClient(method='rtu',port='',stopbit=1,bytesize=8,parity='N',baudrate='9600',timeout=0.3)
connection = Client.connect()
print(connection)
value = Client.read_imput_registers(1000,8,unit=0x01)
print(value.registers)
