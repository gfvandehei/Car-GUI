from queue import Queue

class SensorDatapipe(object):

    def __init__(self):
        self.state = 0
        self.close = False
        self.ondata_callbacks = []
        self.onstate_callbacks = []

    def register_ondata_callback(self, callback: callable):
        self.ondata_callbacks.append(callback)

    def register_onstate_callback(self, callback: callable):
        self.onstate_callbacks.append(callback)
    
    def fire_ondata(self, data: bytes):
        for call in self.ondata_callbacks:
            call(data)

    def change_state(self, state):
        self.state = state
        for call in self.onstate_callbacks:
            call(state)

    def send_command(self, commanddata: bytes):
        print("[WARNING] command not sent in Datapipes base class")
        pass