"""
TCP-client collect the information about internet traffic on PC
every 60 seconds and send in on the server.

For cancel the program running press Ctrl+Q.
"""
import keyboard
import psutil
import socket
import time


running = False


def traffic_info(interval=60):
    """
    Collect the information about internet traffic.

    :param interval: interval (in seconds) of sending
                     information to the server
    """

    global running
    running = True
    start_time = time.time()
    while running:
        prev_recv_bytes = psutil.net_io_counters(pernic=False).bytes_recv
        start_sent_bytes = psutil.net_io_counters(pernic=False).bytes_sent

        while time.time() - start_time < interval and running:
            time.sleep(1)

        if not running:
            break
        recv_bytes = (psutil.net_io_counters(pernic=False).bytes_recv
                      - prev_recv_bytes)
        send_bytes = (psutil.net_io_counters(pernic=False).bytes_sent
                      - start_sent_bytes)
        cur_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        message_recv_bytes = f'{cur_time} - Bytes received: {recv_bytes}\n'
        message_sent_bytes = f'{cur_time} - Bytes sent: {send_bytes}\n'

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(('localhost', 9090))
            # print(f'Send: {message_recv_bytes}')
            sock.send(message_recv_bytes.encode('utf-8'))
            # print(f'Send: {message_sent_bytes}')
            sock.send(message_sent_bytes.encode('utf-8'))

        start_time += interval


def graceful_teardown():
    """Stop collect the information and close connection with server."""
    answer = input('Do you really want stop running? [Y/N]')
    if answer in ['Y', 'y']:
        global running
        running = False


if __name__ == '__main__':
    keyboard.add_hotkey('Ctrl + Q', graceful_teardown)
    print('Start collecting traffic information\n'
          'For cancel press Ctrl+Q')
    traffic_info(5)
