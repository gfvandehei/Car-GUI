import inspect
from lib.app.sensors.sensor import Sensor


class SensorDetector(object):

    def __init__(self):
        self.on_connect_callbacks = []
    
    def register_connection_listener(self, callback: callable):
        if not inspect.ismethod(callback):
            raise(AssertionError("Callback is expected to be a function"))
        signature = inspect.signature(callback)
        #print(list(signature.parameters))
        tlist = list(signature.parameters)
        if signature.parameters[tlist[0]].annotation != Sensor:
            raise(AssertionError("Attributes {} does not match (__:Sensor)".format(str(signature))))
        # check callback args
        self.on_connect_callbacks.append(callback)
    
    def fire_connect_event(self, sensor: Sensor):
        for callback in self.on_connect_callbacks:
            #print("Calling callback", callback)
            callback(sensor)