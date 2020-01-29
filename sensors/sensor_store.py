from os import path
import json

class SensorStore(object):

    def __init__(self, sensor_io_file:str="sensor_map.json", logger=None):
        self.sensor_io_filename = sensor_io_file
        self.sensor_map = self.initialize_file(sensor_io_file) #map of sensor id to array of value pairs

    def initialize_file(self, sensor_file: str):
        #check if file already exists
        sensor_file_descriptor = None
        sensor_file_contents = None
        if(path.isfile(sensor_file)):
            try:
                sensor_file_descriptor = open(sensor_file, "r")
                sensor_file_contents = json.load(sensor_file_descriptor)
            except:
                sensor_file_contents = {}
        else:
            sensor_file_contents = {}

        sensor_file_descriptor.close()
        return sensor_file_contents

    def synch_file_map(self):
        sensor_file = open(self.sensor_io_filename, 'w')
        json.dump(self.sensor_map, sensor_file)

    def write_sensor_data(self, sensor_id:str, sensor_data:tuple):
        if(self.sensor_map.get(sensor_id)):
            self.sensor_map[sensor_id].append(sensor_data)
        else:
            self.sensor_map[sensor_id] = []
            self.sensor_map[sensor_id].append(sensor_data)
        self.synch_file_map()

    def clear_sensor_data(self, sensor_id=None):
        if(sensor_id):
            print("CLEARING SENSOR {}".format(sensor_id))
            self.sensor_map[sensor_id] = []
        else:
            print("CLEARING ENTIRE SENSOR MAP")
            self.sensor_map = {}
        self.synch_file_map()
        
