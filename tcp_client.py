import random
import socket
import time


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 9090))

data = [random.uniform(30, 80) for _ in range(10)]

for item in data:
    time.sleep(2)
    curr_time = time.localtime()
    curr_time = time.strftime('%Y-%m-%d %H:%M:%S', curr_time)
    print(f'Send: {curr_time}: {item:.2f}\n')
    sock.send(f'{curr_time}: Client 1 - {item:.2f}\n'.encode('utf-8'))

sock.close()
