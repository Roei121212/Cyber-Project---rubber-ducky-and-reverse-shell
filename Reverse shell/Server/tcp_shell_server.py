import pickle
import socket
import time

import constants
import network_utils
import lz4.frame
import cv2
import shared_variable_flags


def tcp_shell_server_func():

    while True:
        server_socket = socket.socket()
        server_socket.bind((constants.IP, constants.TCP_SHELL_SERVER_PORT))
        server_socket.listen()
        print("server is up and running")

        while True:
            client, address = server_socket.accept()
            print(f"{address} connected")
            cv2.namedWindow("Live", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("Live", 800, 900)
            while True and shared_variable_flags.tcp_server_on_flag:
                try:
                    time.sleep(0.001)
                    size = client.recv(6)
                    size = size.decode()
                    size = int(size)
                    client.send("send frame".encode())
                    frame = network_utils.recv_all(client, size)
                    frame = lz4.frame.decompress(frame)
                    frame = pickle.loads(frame)
                    cv2.imshow('Live', frame)
                    if cv2.waitKey(1) == ord('q'):
                        cv2.destroyAllWindows()
                        client.close()
                        shared_variable_flags.tcp_server_on_flag = False
                        return
                except Exception as e:
                    pass

            cv2.destroyAllWindows()
            client.close()
            shared_variable_flags.tcp_server_on_flag = False
            return


