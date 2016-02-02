#!/usr/bin/python3

import serial
import time


def main():
    ser = serial.Serial('/dev/ttyUSB1', baudrate=115200)

    # -- Reset Simplez
    ser.setDTR(1)
    time.sleep(0.2)
    ser.setDTR(0)

# -- Main program
if __name__ == '__main__':
    main()
