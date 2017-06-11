import socket
target_host = "127.0.0.1"
target_port = 80

# Create
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Send
client.sendto("AAABBBCCC",(target_host,target_port))

# Recieve
data, addr = client.recvfrom(4096)

print(data, addr)
