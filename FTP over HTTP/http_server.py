import socket
import constants


def parse_http_request(data: str) -> str | None:
    try:
        lines = data.split('\r\n')
        request_line = lines[0]
        return request_line
    except None:
        pass
    return None


def handle_http_request(path: str) -> bytes:
    if path == '/':
        with open(constants.GIF, 'rb') as f:
            file_content = f.read()
        content_type = "image/gif"
        content_length = len(file_content)
        headers = f'HTTP/1.1 200 OK\r\n' \
                  f'Content-Type: {content_type}\r\n' \
                  f'Content-Length: {content_length}\r\n\r\n'
        response = headers.encode() + file_content
    elif path == '/file':
        print("file")
        with open(constants.FILE_NAME, 'rb') as f:
            file_content = f.read()
        content_type = "application/vnd.microsoft.portable-executable"
        content_length = len(file_content)
        headers = f'HTTP/1.1 200 OK\r\n' \
                  f'Content-Type: {content_type}\r\n' \
                  f'Content-Length: {content_length}\r\n' \
                  f'Content-Disposition: attachment; filename="main.exe"\r\n\r\n'
        response = headers.encode() + file_content
    else:
        response = 'HTTP/1.1 404 Not Found\r\n\r\n'.encode()
    return response


class HttpServer:
    def __init__(self):
        self.port = constants.PORT
        self.ip = constants.IP
        self.server_socket = socket.socket()
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen()
        self.client_address = None
        self.client_socket = None
        # print("initiated new server")

    def start_server(self):
        # print("starting new server")
        while True:
            try:
                self.client_socket, self.client_address = self.server_socket.accept()
            except None:
                pass
            while True:
                try:
                    data = self.client_socket.recv(constants.DEFAULT_BUFFER_SIZE)
                    data = data.decode()
                    method, path, http_version = parse_http_request(data).split(' ')
                    response = handle_http_request(path)
                    self.client_socket.sendall(response)
                    self.client_socket.close()
                    break
                except None:
                    pass
