from lib.sensors.basesensor import BaseSensor
import socket
import cv2
import base64
import numpy as np
import time
from threading import Thread

class FakeCameraSensor(BaseSensor):

    def __init__(self, image_file: str, chunk_size: int, *args):
        super().__init__(*args)
        self.mytype = 2
        self.end_f = False

        self.chunk_size = chunk_size
        
        image = cv2.imread(image_file)
        retval, buffer = cv2.imencode('.jpg', image)
        self.img_as_text = base64.b64encode(buffer)
        self.image_send_thread = Thread(target=self.get_pic_thread)
        print(len(image)/self.chunk_size)

    def split_image(self):
        current_chunk_start = 0
        chunks = []
        while True:
            if current_chunk_start+self.chunk_size < len(self.img_as_text):
                chunk = self.img_as_text[current_chunk_start: current_chunk_start+self.chunk_size]
                current_chunk_start = self.chunk_size+current_chunk_start
                chunks.append(chunk)
            else:
                chunk = self.img_as_text[current_chunk_start: len(self.img_as_text)]
                chunks.append(chunk)
                break
        return chunks
    
    def get_pic_thread(self):
        while not self.end_f:
            for i in self.split_image():
                self.send_message(i)
            time.sleep(1/60)

    def run(self):
        self.image_send_thread.start()
        super().run()



