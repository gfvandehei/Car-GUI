# Network Messaging in JEEP GUI

## Sensor Connection Protocol
All of the code regarding the detection of new sensors over the network is in
lib/sensors/sensor_detector_network.py

NetworkSensorDetector looks for messages in the format:   
**| 8 byte id | 8 byte TCP port | 1 byte sensor type code |**  
on a port specified in the config json provided with Core.config

On receiving this message, a new sensor object is created if there are no sensors that already
exist with a matching ID. After creation of the new object a TCP connection is initiated from 
here to the sensor at the provided 8 byte tcp port and address that the original message was received

This TCP connection is text based, messages are delimited by \n.  
All messages transmitted by the sensor will be in the style of {value},{value},*


