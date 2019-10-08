import socket


def connect_to_ui():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 6000
    while True:
        s.connect((host, port))
        print("Connection has been established from ui ")
        break
    return s
