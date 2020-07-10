import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('localhost', 9090))
sock.listen(2)


output_file = 'data.txt'

while True:
    client, addr = sock.accept()
    while True:
        data = client.recv(1024).decode('utf-8')
        if not data:
            break
        with open(output_file, 'a') as f:
            f.writelines(data)
            print(data)
    client.close()
