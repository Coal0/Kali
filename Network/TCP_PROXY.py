import sys
import socket
import threading


def server_loop(lhost, lport, rhost, rport, receive_first):
    server = socket.socket()
    try:
        server.bind((lhost, lport))
    except:
        print("[!] Failed to listen on {}:{}".format(lhost, lport))
        print("[!] Check for other listening sockets or correct permissions")
        sys.exit(1)

    print("[*] Listening on {}:{}".format(lhost, lport))
    server.listen(5)

    while True:
        client_socket, addr = server.accept()
        print("[==>] Received incoming connection from {}:{}".format(
            addr[0], addr[1]))
        proxy_thread = threading.Thread(target=proxy_handler, 
            args=(client_socket, rhost, rport, receive_first))
        proxy_thread.start()


def proxy_handler(client_socket, rhost, rport, receive_first):
    remote_socket = socket.socket()
    remote_socket.connect((rhost, rport))

    if receive_first:
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)
        remote_buffer = response_handler(remote_buffer, True)

        if remote_buffer:
            print("[<==] Sending {} bytes to localhost".format(len(
                remote_buffer)))
            client_socket.sendall(remote_buffer.encode())

    # Loop: 
    # read from local
    # => send to local 
    # => send to remote
    # => send to local

    while True:
        local_buffer = receive_from(client_socket)
        # Read from local

        if local_buffer:
            print("[==>] Received {} bytes from localhost".format(
                len(local_buffer)))
            hexdump(local_buffer)
            local_buffer = request_handler(local_buffer, True)
            remote_socket.sendall(local_buffer.encode())
            print("[==>] Sent to remote")

        remote_buffer = receive_from(remote_socket)
        # Read from remote
        if remote_buffer:
            print("[==>] Received {} bytes from localhost".format(
                len(remote_buffer)))
            hexdump(remote_buffer)
            remote_buffer = request_handler(remote_buffer, True)
            client_socket.sendall(remote_buffer.encode())
            print("[<==] Sent to localhost")

        if not (local_buffer or remote_buffer):
            client_socket.close()
            remote_socket.close()
            print("[*] No more data, closing connections")
            break


def hexdump(source, length=16):
    result = []
    digits = 4 if isinstance(source, unicode) else 2

    if sys.version_info.major < 3:
        for i in xrange(0, len(source), length):
            s = source[i:i+length]
            hexa = b" ".join(["%0*X" % (digits,ord(x)) for x in s])
            text = b"".join([x if 0x20 <= ord(x) < 0x7F else b"." for x in s])
            result.append(
                b"%04X %-*s   %s" % (i, length*(digits+1), hexa, text))
    else:
        for i in range(stop=len(source), step=length):
            s = source[i:i+length]
            hexa = b" ".join(["%0*X" % (digits,ord(x)) for x in s])
            text = b"".join([x if 0x20 <= ord(x) < 0x7F else b"." for x in s])
            results.append(
                b"%04X %-*s   %s" % (i, length*(digits+1), hexa, text))
    print(b"\n".join(result))


def receive_from(connection, timeout=2):
    buffer = ""
    connection.settimeout(timeout)
    try:
        while True:
            data = connection.recv(4096)
            if not data:
                # Connection closed
                break
            buffer += data
    except socket.error:
        pass
    return buffer


def request_handler(buffer, ignore_not_yet_implemented=False):
    if not ignore_not_yet_implemented:
        raise NotImplementedError
    return buffer


def response_handler(buffer, ignore_not_yet_implemented=False):
    if not ignore_not_yet_implemented:
        raise NotImplementedError
    return buffer


def main():
    USAGE = """
Usage:
    python TCP_PROXY.py [localhost] [localport]\
 [remotehost] [remoteport] [receive first]
Example:
    python TCP_PROXY.py 127.0.0.1 9000 10.12.132.1 9000 True
    """
    if len(sys.argv[1:]) != 5:
        print(USAGE)
        sys.exit(1)

    local_host = sys.argv[1]
    try:
        local_port = int(sys.argv[2])
    except ValueError:
        print("Local port must be a number.")
        sys.exit(1)

    remote_host = sys.argv[3]
    try:
        remote_port = int(sys.argv[4])
    except ValueError:
        print("Remote port must be a number.")
        sys.exit(1)

    if sys.argv[5] == "True":
        receive_first = True
    else:
        receive_first = False
        
    server_loop(local_host,
                local_port,
                remote_host,
                remote_port,
                receive_first)

if __name__ == "__main__":
    main()

