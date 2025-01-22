import serial
import time
import pyaudio

# Serial Ports for AT commands and Audio data
s_AT = serial.Serial('/dev/ttyUSB2', 115200, timeout=1)
s_Audio = serial.Serial('/dev/ttyUSB4', 115200, timeout=1)

# Send AT Command and Check Response
def send_at_command(command):
    s_AT.write(f"{command}\r\n".encode())
    time.sleep(0.1)
    response = s_AT.read(s_AT.in_waiting).decode(errors="ignore")
    print(f"Command: {command}, Response: {response}")
    return response

# Initialize PyAudio
p = pyaudio.PyAudio()

# Callback Function for Input Audio
def pcm_out(in_data, frame_count, time_info, status):
    try:
        s_Audio.write(in_data)
    except Exception as e:
        print(f"Error streaming audio: {e}")
    return (in_data, pyaudio.paContinue)

try:
    # Start Call
    print("Initializing call...")
    send_at_command("AT")
    send_at_command("ATD8153841347;")  # Replace with the correct phone number
    send_at_command("AT+CPCMREG=1")  # Enable PCM

    # Setup Audio Streams
    print("Setting up audio streams...")
    stream_out = p.open(format=p.get_format_from_width(2),
                        channels=1,
                        rate=8000,
                        output=True)

    stream_in = p.open(format=p.get_format_from_width(2),
                       channels=1,
                       rate=8000,
                       input=True,
                       stream_callback=pcm_out)

    stream_in.start_stream()
    print("Streaming audio... Press Ctrl+C to stop.")

    # Read and Play Audio
    while True:
        if s_Audio.in_waiting > 0:
            pcm_data = s_Audio.read(s_Audio.in_waiting)
            stream_out.write(pcm_data)

except KeyboardInterrupt:
    print("Streaming interrupted by user.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Clean up Resources
    print("Releasing resources...")
    if stream_in.is_active():
        stream_in.stop_stream()
        stream_in.close()
    if stream_out.is_active():
        stream_out.stop_stream()
        stream_out.close()

    p.terminate()
    s_Audio.close()
    s_AT.close()
    print("Resources released. Audio streaming ended.")
