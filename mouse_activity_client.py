"""
TCP-client collect the information about mouse activity on PC
every 60 seconds and send in on the server.

For cancel the program running press Ctrl+X.
"""
import keyboard
import socket
import time
from pynput import mouse


running = False
mouse_left_clicks = 0
# mouse_usage = 0

ms = mouse.Controller()


def mouse_activity_info(interval=60):
    """
    Collect the information about movements of mouse.

    :param interval: interval (in seconds) of sending
                     information to the server
    """

    global mouse_left_clicks
    global running
    running = True
    start_time = time.time()
    while running:
        prev_left_clicks = mouse_left_clicks
        mouse_usage = 0
        prev_pos = ms.position

        while time.time() - start_time < interval and running:
            time.sleep(1)
            cur_position = ms.position
            if cur_position != prev_pos:
                mouse_usage += 1
                prev_pos = cur_position

        if not running:
            break
        left_clicks = mouse_left_clicks - prev_left_clicks
        mouse_usage = mouse_usage / interval * 100
        cur_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        message_left_clicks = f'{cur_time} - Left clicks: {left_clicks}\n'
        message_mouse_usage = f'{cur_time} - Mouse usage: {mouse_usage:.2f} %\n'

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', 9090))
        # print(f'Send: {message_left_clicks}')
        sock.send(message_left_clicks.encode('utf-8'))
        # print(f'Send: {message_mouse_usage}')
        sock.send(message_mouse_usage.encode('utf-8'))
        sock.close()

        start_time += interval


def on_click(x, y, button, pressed):
    """Callback for the listener with count the left mouses clicks."""
    global mouse_left_clicks
    if pressed and button == mouse.Button.left:
        mouse_left_clicks += 1


def graceful_teardown():
    """Stop collect the information and close connection with server."""
    global running
    answer = input('Do you really want stop running? [Y/N]')
    if answer in ['Y', 'y']:
        running = False


if __name__ == '__main__':
    keyboard.add_hotkey('Ctrl + X', graceful_teardown)
    print('Start collecting mouses activity information\n'
          'For stop program press Ctrl+X')

    listener = mouse.Listener(on_click=on_click)
    listener.setDaemon(daemonic=True)
    listener.start()

    mouse_activity_info(10)
