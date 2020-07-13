"""
TCP-server receive the information from some TCP-client
and save it in the file 'data.txt'.
"""
import socket
import time
from multiprocessing.pool import ThreadPool


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('localhost', 9090))
sock.listen(2)


output_file = 'data.txt'

pool = ThreadPool(4)


def handle_client(cl):
    while True:
        data = cl.recv(1024).decode('utf-8')
        if not data:
            break
        with open(output_file, 'a') as f:
            f.writelines(data)
            print(data)
    cl.close()


if __name__ == '__main__':
    start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    print(f'\nServer start working: {start_time}')
    while True:
        client, addr = sock.accept()
        pool.apply_async(handle_client, (client,))
