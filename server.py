import socket
import threading
import cv2
import pyaudio
import numpy as np
import struct

# Server configuration
clients = []
UDP_PORT_SEND = 5005
sock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Video Capture Setup
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Set resolution for video capture
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

# Audio Setup (higher quality)
p = pyaudio.PyAudio()
audio_stream = p.open(format=pyaudio.paInt16, channels=2, rate=16000, input=True, frames_per_buffer=512)  # Stereo at 16 kHz

print("Server is running, waiting for clients...")

# Accepting connections from clients
def receive_connections():
    while True:
        try:
            addr = (input("Enter client's IP: "), UDP_PORT_SEND)
            if addr not in clients:
                clients.append(addr)
                print(f"New client connected: {addr}")
        except Exception as e:
            print(f"Error receiving connection: {e}")

threading.Thread(target=receive_connections, daemon=True).start()

# Streaming video and audio
def stream_data():
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame.")
            break

        # Use JPEG encoding for video
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 30]  # Reduce quality to 30
        _, buffer = cv2.imencode('.jpg', frame, encode_param)
        video_data = buffer.tobytes()

        # Read audio data from microphone
        audio_data = audio_stream.read(512)  # Adjusted chunk size

        # Create a combined packet with video and audio lengths
        video_length = len(video_data)
        audio_length = len(audio_data)

        # Error check for data sizes
        if video_length > 8000 or audio_length > 8000:
            print("Error: Video or audio data exceeds the maximum allowed size.")
            continue

        # Create the packet to send: packet type (0), video length, audio length, video data, audio data
        packet = struct.pack('B I I', 0, video_length, audio_length) + video_data + audio_data

        # Send packet to all connected clients
        for client in clients:
            try:
                sock_send.sendto(packet, client)
                print(f"Sent packet to {client}")
            except Exception as e:
                print(f"Error sending packet to {client}: {e}")

        # Show the video stream on the server side
        cv2.imshow("Server Stream", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Start video and audio streaming in a separate thread
threading.Thread(target=stream_data, daemon=True).start()

# Main loop to keep the server running
try:
    while True:
        pass
except KeyboardInterrupt:
    print("Server shutting down...")
    # Cleanup resources when the server is stopped
    cap.release()
    audio_stream.stop_stream()
    audio_stream.close()
    sock_send.close()
    cv2.destroyAllWindows()