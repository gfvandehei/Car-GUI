import inspect


class SensorDetector(object):

    def __init__(self):
        self.on_connect_callbacks = []
    
    def register_connection_listener(self, callback: callable):
        if not inspect.ismethod(callback):
            raise(AssertionError("Callback is expected to be a function"))
        signature = inspect.signature(callback)
        print(list(signature.parameters))
        tlist = list(signature.parameters)
        if signature.parameters[tlist[0]].annotation != int or signature.parameters[tlist[1]].annotation != int or\
                signature.parameters[tlist[2]].annotation != int or signature.parameters[tlist[3]].annotation != (str, int):
            raise(AssertionError("Attributes {} does not match (int, int, int, (str, int))".format(str(signature))))
        # check callback args
        self.on_connect_callbacks.append(callback)
    
    def fire_connect_event(self, sensor_id: int, sensor_tcp_port: int, 
                           sensor_type: int, sensor_address: (str, int)):
        for callback in self.on_connect_callbacks:
            print("Calling callback", callback)
            callback(sensor_id, sensor_tcp_port, sensor_type, sensor_address)