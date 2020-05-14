import socket

HOST = '192.168.1.35'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

# server socket initialized
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    # s.accept() makes a new socket for each connection
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            # sending the receiving data
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
