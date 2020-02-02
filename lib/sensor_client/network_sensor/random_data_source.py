import random
from threading import Thread
from lib.sensor_client.network_sensor.datasource import DataSource
import time


class RandomDataSource(DataSource):

    def __init__(self):
        super().__init__()
        self.t_red = Thread(target=self.random_source_thread)
        self.t_red.start()

    def random_source_thread(self):
        while True:
            random_num = random.randint(0, 100)
            self.propagate([random_num])
            time.sleep(1)