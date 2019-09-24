import socket


def connect():
    # server_socket = socket.socket()
    # server_socket.bind(('0.0.0.0', 8000))
    # server_socket.listen(0)
    # return server_socket.accept()[0].makefile('wb')
    port = 60000  # Reserve a port for your service.
    s = socket.socket()  # Create a socket object
    host = socket.gethostname()  # Get local machine name
    # host = 'localhost'  # Get local machine name
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))  # Bind to the port
    s.listen(5)  # Now wait for client connection.
    print('Server listening....')
    # while True:
    conn, addr = s.accept()  # Establish connection with client.
    print('Got connection from', addr)
    return conn
