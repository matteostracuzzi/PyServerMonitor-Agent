from threading import Thread
from time import sleep
from main import settings
from datetime import datetime
import psutil, platform

class Retriever(Thread):
    def __init__(self, sender) -> None:
        super().__init__(daemon=False)
        self.sender = sender

    def start(self):
        while True:
            data = self.retrieve_data()
            self.sender.send(data)
            sleep(settings['update_time'])


    @classmethod
    def retrieve_data(cls)->dict:
        data = {}
        for info in settings['enabled_info']:
            if info == 'cpu':
                data.update(cls.get_cpu_info())
            elif info == 'uptime':
                data.update(dict(uptime = (datetime.now()-datetime.fromtimestamp(psutil.boot_time())/60/60)))
            elif info == 'os':
                data.update(dict(os = f'{platform.uname().system} {platform.uname.version}'))
        return data

    @property
    def get_cpu_info(cls)->dict:
        data = {
            'cpu_use': psutil.cpu_percent(),
            'cpu_freq': round(psutil.cpu_freq().current,2),
            'cpu_threads': psutil.cpu_count(),
            'cpu_cores': psutil.cpu_count(logical=False),
            'architecture': platform.uname.machine
        }
        return data
    
