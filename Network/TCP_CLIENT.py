import sys
import socket

TARGET_HOST = "0.0.0.0"
TARGET_PORT = 9999

if __name__ == "__main__":
    client = socket.socket()
    client.connect((TARGET_HOST, TARGET_PORT))
    if sys.version_info.major < 3:
        request = raw_input("What do we want to send >>> ")
    else:    
        request = input("What do we want to send >>> ").encode()
    client.send(request)
    while True:
        response = client.recv(4096)
        if not response:
            break
        print(response)
