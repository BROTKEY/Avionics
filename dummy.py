import socket
from time import sleep

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while True:
    for i in range(1,20):
        sock.sendto(bytes(f"{i**2},-{i**2},{i*10}", 'utf-8'), ("127.0.0.1",3000))
        sleep(0.1)
    for i in reversed(range(19)):
        sock.sendto(bytes(f"{i**2},-{i**2},{i*10}", 'utf-8'), ("127.0.0.1",3000))
        sleep(0.1)