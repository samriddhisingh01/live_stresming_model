import socket
import cv2
import numpy as np
import pyaudio
import threading
import struct

# Client configuration
UDP_IP = "0.0.0.0"  # Listen on all interfaces
UDP_PORT = 5005  # Port to match the server
CHUNK = 512  # Audio chunk size

# Audio setup (higher quality)
p = pyaudio.PyAudio()
audio_stream = p.open(format=pyaudio.paInt16, channels=2, rate=16000, output=True,
                      frames_per_buffer=CHUNK)  # Stereo at 16 kHz

# Create a UDP socket to receive video and audio data
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print("Client is ready to receive video and audio...")

def receive_data():
    while True:
        try:
            # Receive packet from the server
            packet, addr = sock.recvfrom(65507)

            # Check if the packet is large enough to unpack header information
            if len(packet) < 12:
                print(f"Received packet too small: {len(packet)} bytes")
                continue

            # Unpack the header: packet type, video length, audio length
            packet_type, video_length, audio_length = struct.unpack('B I I', packet[:12])

            # Ensure the total packet size matches expected lengths
            total_expected_length = 12 + video_length + audio_length
            if len(packet) < total_expected_length:
                print(f"Received packet size ({len(packet)}) does not match expected length ({total_expected_length})")
                continue

            # Extract the video and audio data
            video_data = packet[12:12 + video_length]
            audio_data = packet[12 + video_length:]

            # Process the video data
            np_data = np.frombuffer(video_data, np.uint8)
            frame = cv2.imdecode(np_data, cv2.IMREAD_COLOR)
            if frame is not None:
                cv2.imshow("Client Stream", frame)

            # Play the audio
            audio_stream.write(audio_data)

            # Exit if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        except Exception as e:
            print(f"Error receiving data: {e}")
            break

# Start the video/audio receiving thread
threading.Thread(target=receive_data, daemon=True).start()

# Keep the client running
try:
    while True:
        pass
except KeyboardInterrupt:
    print("Client shutting down...")
    # Clean up resources
    sock.close()
    audio_stream.stop_stream()
    audio_stream.close()
    p.terminate()
    cv2.destroyAllWindows()
