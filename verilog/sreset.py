import serial
import time

ser = serial.Serial('/dev/ttyUSB1', baudrate=115200)

# -- Reset Simplez
ser.setDTR(1)
time.sleep(0.2)
ser.setDTR(0)
