import sys
from lib.sensors.climate_sensor.network_client.climatesensor import ClimateSensor

if len(sys.argv) < 4:
    print("Usage: climate_sensor.py <id: int> <server_port: int> <serial_port: str>")

myid = int(sys.argv[1])
host_location = int(sys.argv[2])
if len(sys.argv) > 3:
    serial_location = str(sys.argv[3])
else:
    serial_location = None

ClimateSensor(mid=myid, host_port=host_location, serial_port=serial_location)

