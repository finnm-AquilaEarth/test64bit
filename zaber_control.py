# This script enables the user to move a Zaber device by a specified distance.

from zaber_motion import Library
from zaber_motion.ascii import Connection
import socket
import time

# Initialize the Zaber library
Library.enable_device_db_store()

port = "COM4"  # Adjust for your system
distance = 10


# Function to move the device by the given distance
def move_device_by_distance(distance, port_num):
    # Open connection to the Zaber device (replace '/dev/ttyUSB0' with your actual port)
    with Connection.open_serial_port(port_num) as connection:  # Adjust for your system
        devices = connection.detect_devices()

        if len(devices) == 0:
            print("No devices found.")
            return

        device = devices[0]
        axis = device.get_axis(1)

        # Move by the given distance
        print(f"Moving by {distance} units.")
        axis.move_relative(distance, unit="mm", acceleration=5)

        # Get the current position after the move
        position = axis.get_position()
        print(f"Current position: {position}")

        # Get the current position in mm
        position_mm = axis.get_position(unit="mm")
        print(f"Current position in mm: {position_mm}")

def move_gantry(conn: socket):

    # Move the device by the given distance
    move_device_by_distance(distance, port)

    message = "Gantry finished moving"
    conn.sendall(message.encode())

def return_home(port_num):
    with Connection.open_serial_port(port_num) as connection:  # Adjust for your system
        devices = connection.detect_devices()

        if len(devices) == 0:
            print("No devices found.")
            return

        device = devices[0]
        axis = device.get_axis(1)
        axis.home()
    
    


    
