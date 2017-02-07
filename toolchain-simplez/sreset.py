#!/usr/bin/python3

import serial
import time
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="Send reset signal to Simplez from serial port")
    parser.add_argument("-p", "--port", default='/dev/ttyUSB0', help="Port for serial terminal", action="store")
    args = parser.parse_args()
    try:
        ser = serial.Serial(args.port, baudrate=115200)
    except:
        print("Error: Serial port not found: {}".format(args.port))
        sys.exit(0)

    # -- Reset Simplez
    ser.setDTR(1)
    time.sleep(0.2)
    ser.setDTR(0)

# -- Main program
if __name__ == '__main__':
    main()
