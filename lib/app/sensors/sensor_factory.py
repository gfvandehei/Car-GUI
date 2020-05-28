import struct
from lib.app.sensors.sensor import Sensor
from lib.app.sensors.sensor_types.climate_sensor import ClimateSensor
from lib.app.sensors.sensor_types.camera_sensor import CameraSensor

class SensorFactory(object):

    _sensors: dict = {}
    _await_functions: list = []

    """
    triggers any functions awaiting for a sensor to connect
    """
    @classmethod
    def _trigger_await(cls, sid, sensor):
        for await_function_pair in cls._await_functions:
            if await_function_pair[0] == sid:
                await_function_pair[1](sensor)
                cls._await_functions.remove(await_function_pair)
            else:
                continue
    
    """
    allows an object to await on a sensor to connect, if the sensor is already connected it is
    returned immediatly, otherwise the function will run when it connects
    """
    @classmethod
    def await_sensor(cls, sensor_id: int, on_sensor: callable):
        if cls._sensors.get(sensor_id) is not None:
            on_sensor(cls._sensors[sensor_id])
        else:
            cls._await_functions.append((sensor_id, on_sensor))

    @classmethod
    def post_sensor_update(cls, message_data: bytes):
        sensor_id, sensor_type = struct.unpack("!IH", message_data[0:6])
        print("DEBUG: message", sensor_id, sensor_type)

        if cls._sensors.get(sensor_id) is not None:
            sensor: Sensor = cls._sensors.get(sensor_id)
            sensor.parse_data(message_data[6:])
        else:
            switch = {
                1: ClimateSensor,
                2: CameraSensor
            }
            sensor_class = switch.get(sensor_type, Sensor)
            if sensor_class is Sensor:
                print("Received update from sensor of type {} which does not yet exist".format(sensor_type))
                print("using default sensor")
            new_sensor: Sensor = sensor_class(sensor_id)
            new_sensor.receive_update(message_data[6:])
            print("DEBUG: created sensor", new_sensor)
            cls._sensors[sensor_id] = new_sensor
            cls._trigger_await(sensor_id, new_sensor)