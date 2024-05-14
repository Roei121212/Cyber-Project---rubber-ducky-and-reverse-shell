import socket
import threading
import time
import shared_variable_flags
import constants
import tcp_shell_server
import tkinter as tk
import network_utils

clients = []

LOCAL_IP = network_utils.find_local_ipv4addr()

try:
    server_socket = socket.socket()
    server_socket.bind((constants.IP, constants.CONFIG_SERVER_PORT))
    server_socket.listen()
    print("server is up and running")

except socket.error as error:
    pass


def handle_client():
    while True:
        try:
            client, address = server_socket.accept()
            print(address, "has connected")
            clients.append(client)
        except:
            pass


def check_connection(client_socket):
    print("checking", client_socket)
    try:
        client_socket.send("UP".encode())
    except Exception as e:
        print(e)
        return False
    client_socket.settimeout(10)
    try:
        data = client_socket.recv(1024)
        if data.decode() == "UP":
            print("valid")
            return True
    except Exception as e:
        print(e)
        return False


def check_all_connections():
    while True:
        for c in clients:
            time.sleep(4)
            if not (check_connection(c)):
                clients.remove(c)


def printer():
    while True:
        time.sleep(2)
        # print(clients)


saved_client = None


def on_select(event):
    global saved_client
    selected_index = listbox.curselection()[0]
    selected_item = clients[selected_index]
    saved_client = selected_item
    print(saved_client)

    return None


def update_listbox():
    listbox.delete(0, tk.END)
    for item in clients:
        listbox.insert(tk.END, item)


def auto_update():
    update_listbox()
    root.after(200, auto_update)


def run_threads():
    t1 = threading.Thread(target=printer)
    t1.start()

    t2 = threading.Thread(target=check_all_connections)
    t2.start()

    t3 = threading.Thread(target=handle_client)
    t3.start()


def close_popup():
    menu.unpost()


def connect():
    global saved_client
    saved_client.send("START_STREAM".encode())
    saved_client.send(
        f"{str(network_utils.find_local_ipv4addr())}:{str(constants.TCP_SHELL_SERVER_PORT)}".encode())
    shared_variable_flags.tcp_server_on_flag = True
    if saved_client and shared_variable_flags.tcp_server_on_flag:
        t4 = threading.Thread(target=tcp_shell_server.tcp_shell_server_func)
        t4.start()


def disconnect():
    shared_variable_flags.tcp_server_on_flag = False
    global saved_client
    if saved_client:
        saved_client.send("END_STREAM".encode())


root = tk.Tk()
menu = tk.Menu(root, tearoff=False)
menu.add_command(label='connect', command=connect)
menu.add_command(label="disconnect", command=disconnect)
menu.add_command(label="cancel", command=close_popup())


def popup_menu(e):
    menu.tk_popup(e.x_root, e.y_root)


root.bind('<Button-3>', popup_menu)
listbox = tk.Listbox(root, font=("Arial", 12), selectmode=tk.SINGLE)
listbox.pack(pady=10, padx=10, expand=True, fill=tk.BOTH)

update_listbox()

listbox.bind("<<ListboxSelect>>", on_select)

run_threads()
auto_update()

root.mainloop()
