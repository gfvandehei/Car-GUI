class Sensor(object):

    def __init__(self, sensor_id: int):
        self._sensor_id = sensor_id
        self._data_array = []
        self._max_data_points = 200

        self._subscribers = []

    def fully_initialize(self):
        pass

    def get_id(self):
        return self._sensor_id

    def add_data_point(self, data_point):
        if len(self._data_array) > self._max_data_points:
            self._data_array.remove(self._data_array[0])
        self._data_array.append(data_point)
        print(data_point)
        self.update_subscribers()

    def get_most_recent_data_point(self):
        if len(self._data_array) > 0:
            return self._data_array[-1]
        else:
            return None

    def get_most_recent_data_points(self, how_many: int):
        if how_many >= self._max_data_points:
            return self._data_array
        else:
            return self._max_data_points[0-how_many:-1]

    def change_max_data_points(self, new_max:int):
        self._max_data_points = new_max

    def update_subscribers(self):
        for callback in self._subscribers:
            callback(self._data_array[-1])

    def subscribe(self, callback: callable):
        self._subscribers.append(callback)

    def receive_update(self, data_raw):
        self.add_data_point(data_raw)

