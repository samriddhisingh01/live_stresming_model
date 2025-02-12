# Live Video and Audio Streaming Project

## Overview

This project implements a client-server architecture for real-time video and audio streaming over a network. The server captures video and audio data and transmits it to connected clients, which then decode and display the content in real-time.

## How Live Streaming Works

Live streaming involves capturing and transmitting media content in real-time over the internet. The process includes:

1. **Capture**: A camera, microphone, or other recording device captures the content.
2. **Compress and Encode**: The raw data is compressed to remove redundant information and then encoded into a digital format.
3. **Segment**: The data is divided into segments to prevent bottlenecks and save bandwidth.
4. **Transmit**: The server sends the encoded data to connected clients over the network.
5. **Receive and Decode**: Clients receive the data, decode it, and convert it back into video and audio for playback.

The goal is to minimize delay, allowing viewers to experience the content as it is being recorded.

## Live Streaming Process

1. **Connection Establishment**:
   - The server awaits input for client IPs and accepts connections.
   - Clients specify their IP addresses to the server, which stores these for sending video and audio data.

2. **Frame Capture and Transmission**:
   - The server continuously captures frames from the camera and encodes them.
   - It sends the encoded frame data to all connected clients via UDP.

3. **Receiving and Displaying Frames**:
   - Clients listen for incoming data on the specified UDP port.
   - Upon receiving the data, they decode the bytes back into an image format and display it in real-time.

4. **Real-time Performance**:
   - The use of threads allows for simultaneous handling of client connections and video streaming, enabling smooth performance.

## Prerequisites

Ensure the following Python libraries are installed:

- `opencv-python`: For video handling and display.
- `numpy`: For numerical operations.
- `pyaudio`: For audio handling.
- `socket`: Standard library for network communication.
- `threading`: For managing and handling threads.

**Installation**:

```bash
pip install opencv-python numpy pyaudio
