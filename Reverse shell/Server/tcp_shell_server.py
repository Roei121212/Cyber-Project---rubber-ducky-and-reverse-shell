from flask import Flask, render_template, Response
import socket
import constants
import shared_variable_flags


def recv_all(sock, size):
    data = b""
    while len(data) < size:
        chunk = sock.recv(min(size - len(data), 4096))
        if not chunk:
            break
        data += chunk
    return data


def tcp_shell_server_flask(ip: str, port: int):
    app = Flask(__name__)
    server_socket = socket.socket()
    server_socket.bind((ip, port))
    server_socket.listen()

    def generate_frames():
        client, address = server_socket.accept()
        while shared_variable_flags.tcp_server_on_flag:
            try:
                size = int.from_bytes(client.recv(6), byteorder='big')
                if size == 0:
                    break
                frame = recv_all(client, size)
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                print(e)
                break
        client.close()

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/screen')
    def screen():
        return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

    return app


def run_shell_server():
    app = tcp_shell_server_flask(constants.IP, constants.TCP_SHELL_SERVER_PORT)
    if app:
        app.run(threaded=True)
