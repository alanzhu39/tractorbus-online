import socket

client_conns = []

def add_conn(conn):
    client_conns.append(conn)

def get_conn(index):
    return client_conns[index]

def get_length():
    return len(client_conns)