class DataSource(object):

    def __init__(self):
        self.subscribers = []

    def subscribe(self, on_data_callback: callable):
        self.subscribers.append(on_data_callback)

    def propagate(self, data):
        for callback in self.subscribers:
            callback(data)