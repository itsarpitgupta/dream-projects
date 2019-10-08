import socket


def connect_to_camera():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket successfully created")
    except socket.error as err:
        print('socket creation failed with error %s' % (err))
    host = socket.gethostname()
    port = 6000
    s.bind((host, port))
    s.listen(5)
    clientsocket, address = s.accept()
    print('Connection has been established !')
    return clientsocket
