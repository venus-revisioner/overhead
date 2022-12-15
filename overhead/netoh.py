import os
import sys
import time

from requests import get

from overhead.terminaloh import Terminal
from overhead.toolboxoh import text_to_file, log_time


class InetAccessToggle:
    def __init__(self, adapter_name='Ethernet'):
        Terminal().resize()
        self.adapter_name = adapter_name

    def enable(self):
        os.system(f'netsh interface set interface name={self.adapter_name} admin=ENABLED')

    def disable(self):
        os.system(f'netsh interface set interface name={self.adapter_name} admin=DISABLED')

    def toggle(self, adapter_name=None, delay=4):
        if adapter_name is None:
            adapter_name = self.adapter_name
        self.disable()
        print(f'DISABLING "{adapter_name}"...')
        time.sleep(delay)
        print(f'ENABLING "{adapter_name}"...')
        self.enable()
        time.sleep(1)


class MyIP:
    def __init__(self, log_path=None):
        Terminal().resize(21, 42)
        self.ip = get("https://api.ipify.org").text
        self.log_path = log_path

    def __str__(self):
        log_str = self.get_log_str()
        return log_str

    def get_ip(self):
        ip = (f'Public IP address:\n{self.ip}')
        return ip

    def get_log_str(self):
        server_info = f'Logged on: {sys.platform}'
        logged_time = log_time(prefix="")
        log_str = f'{logged_time}\n{server_info}\n{self.get_ip()}\n'
        log_str += "-" * 21
        return log_str

    def save_log(self):
        if self.log_path is None:
            print("NO LOGGING PATH!")
            raise Exception
        else:
            log_str = self.get_log_str()
            text_to_file(self.log_path, log_str, "a+")

    def start_log_loop(self, interval_min=60):
        while True:
            try:
                self.save_log()
                print(self)
                time.sleep(interval_min * 60)
            except KeyboardInterrupt:
                print("EXIT")
                time.sleep(1)
                break
            except Exception:
                print("EXIT")
                time.sleep(1)
                break
