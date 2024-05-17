import subprocess
import sys
import threading
import ctypes
import client_global_flags_a
import cv2
import numpy as np
from PIL import ImageGrab
import socket


def stream_to_server(ip, port):
    if not client_global_flags_a.streaming:
        return
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))

    while client_global_flags_a.streaming:
        screen = ImageGrab.grab()
        frame = np.array(screen)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]
        ret, buffer = cv2.imencode('.jpg', frame, encode_param)
        frame = buffer.tobytes()
        # Send the length of the frame
        s.sendall(len(frame).to_bytes(6, byteorder='big'))
        # Send the frame data
        s.sendall(frame)

    s.close()


'''SW_HIDE = 0


def hide_console():
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), SW_HIDE)


hide_console()
time.sleep(15)'''

my_socket = socket.socket()
my_socket.connect(("10.0.0.12", 44100))
while True:
    print("waiting")
    msg = my_socket.recv(1024).decode()
    print(msg)
    if msg == "UP":
        my_socket.send("UP".encode())
    if msg == "START_STREAM":
        ip_port = my_socket.recv(1024).decode()
        ip = ip_port[:ip_port.index(":")]
        port = int(ip_port[ip_port.index(":") + 1:])
        client_global_flags_a.streaming = True
        t = threading.Thread(target=stream_to_server, args=(ip, port))
        t.start()
    if msg == "END_STREAM":
        client_global_flags_a.streaming = False
