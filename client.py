import socket

with socket.socket() as s:
    s.connect(("localhost", 8080))
    s.send(b"Doei")