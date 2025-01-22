import serial
import sounddevice as sd
import numpy as np

# Configuration
SERIAL_PORT = "COM12"  # Update this to match your Windows COM port (e.g., COM3, COM4)
BAUD_RATE = 115200  # Match with the sender's baud rate
SAMPLE_RATE = 44100  # Match with the sender's sample rate
CHUNK_SIZE = 1024  # Number of frames per buffer

# Initialize serial connection
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)  # Add a timeout for stability
    print(f"Listening on {SERIAL_PORT} at {BAUD_RATE} baud...")
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit()


def audio_callback(outdata, frames, time, status):
    if status:
        print(f"Status: {status}")
    if ser.in_waiting > 0:
        # Read the audio data from the serial port
        data = ser.read(frames * 2)  # Each frame is 2 bytes for 16-bit audio

        # Print the received raw audio data
        print(f"Received USB AudioData: {data[:64]}")  # Print the first 64 bytes for brevity

        # Convert the raw data to audio samples and pass it to the audio stream
        outdata[:] = np.frombuffer(data, dtype=np.int16).reshape(-1, 1)


# Open audio stream
with sd.OutputStream(samplerate=SAMPLE_RATE, channels=1, callback=audio_callback):
    print("Press Ctrl+C to stop...")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Exiting...")
