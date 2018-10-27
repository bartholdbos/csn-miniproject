import socket
import selectors
import types

sel = selectors.DefaultSelector()
message = None
disconnect = None


def server_init(port, message_callback, disconnect_callback):
    global message, disconnect
    message = message_callback
    disconnect = disconnect_callback
    sock = socket.socket()
    sock.bind(("", port))
    sock.listen()
    sock.setblocking(False)
    sel.register(sock, selectors.EVENT_READ, data=None)

    print("Server listening on :" + str(port))


def server_event(sock):
    conn, addr = sock.accept()
    conn.setblocking(False)

    data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE

    sel.register(conn, events, data=data)

    print("Client connected from", addr)


def client_event(key, mask):
    conn = key.fileobj
    data = key.data

    if mask & selectors.EVENT_READ:
        data.inb = conn.recv(1024)

        if data.inb:
            message(data.inb, data.addr)
        else:
            disconnect(data.addr)
            sel.unregister(conn)
            conn.close()

    if mask & selectors.EVENT_WRITE:
        if data.outb:
            sent = conn.send(data.outb)
            data.outb = data.outb[sent:]


def event_loop():
    events = sel.select(timeout=0.1)
    for key, mask in events:
        if key.data is None:
            server_event(key.fileobj)
        else:
            client_event(key, mask)