import keyboard
import socket
import time
from abc import ABC, abstractmethod
from pynput import mouse
from threading import Thread


class MetricCollector(ABC):
    def __init__(self, name):
        self.name = name
        self.value = 0
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._running = False
        self.interval = 60

    def start_collect(self, host, port, interval=60):
        self.sock.connect((host, port))
        self.interval = interval
        self.start_time = time.time()
        self._running = True
        self.loop()

    def get_current_state(self):
        return f'{self.name}: {self.value}'

    def cleanup(self):
        self.value = 0

    def stop_collect(self):
        answer = input(f'Do you really want stop running '
                       f'{self.name} collector? [Y/N]')
        if answer in ['Y', 'y']:
            print(f'{self.name} collector stopped')
            self._running = False

    def loop(self):
        while self._running:
            while (time.time() - self.start_time < self.interval
                   and self._running):
                time.sleep(1)
                self.step()

            if not self._running:
                self.sock.close()
                break
            self.calculate_value()
            cur_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            message = f'{cur_time} - {self.get_current_state()}\n'
            # print(f'Send: {message}')
            self.sock.send(message.encode('utf-8'))
            self.cleanup()
            self.start_time += self.interval

        self.sock.close()

    @abstractmethod
    def calculate_value(self):
        pass

    @abstractmethod
    def step(self):
        pass


class MouseLeftClickCollector(MetricCollector):
    def __init__(self, name):
        super().__init__(name)
        self.listener = mouse.Listener(on_click=self.on_click)
        self.listener.setDaemon(daemonic=True)
    
    def on_click(self, x, y, button, pressed):
        """Callback for the listener with count the left mouses clicks."""
        if pressed and button == mouse.Button.left:
            self.value += 1

    def start_collect(self, host, port, interval=60):
        self.listener.start()
        super().start_collect(host, port, interval)

    def loop(self):
        keyboard.add_hotkey('Ctrl + X', self.stop_collect)
        print(f'Start {self.name} collector\n'
              'For stop running press Ctrl+X\n')
        super().loop()

    def calculate_value(self):
        pass

    def step(self):
        pass


class MouseUsageCollector(MetricCollector):
    def __init__(self, name):
        super().__init__(name)
        self.mouse_usage = 0
        self.ms = mouse.Controller()

    def start_collect(self, host, port, interval=60):
        self._prev_pos = self.ms.position
        super().start_collect(host, port, interval)

    def loop(self):
        keyboard.add_hotkey('Ctrl + Q', self.stop_collect)
        print(f'Start {self.name} collector\n'
              'For stop program press Ctrl+Q\n')
        super().loop()

    def get_current_state(self):
        return f'{super().get_current_state()} s'

    def calculate_value(self):
        # self.value = self.value / self.interval * 100
        pass

    def step(self):
        if self.ms.position != self._prev_pos:
            self.value += 1
            self._prev_pos = self.ms.position


if __name__ == '__main__':
    left_clicks = MouseLeftClickCollector('Mouse left clicks')
    tr_left_clicks = Thread(target=left_clicks.start_collect,
                            args=('localhost', 9090, 5))
    tr_left_clicks.start()

    mouse_usage = MouseUsageCollector('Mouse usage')
    tr_mouse_usage = Thread(target=mouse_usage.start_collect,
                            args=('localhost', 9090, 10))
    tr_mouse_usage.start()

    tr_left_clicks.join()
    tr_mouse_usage.join()
