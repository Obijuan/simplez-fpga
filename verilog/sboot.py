#!/usr/bin/python3

import serial
import time

# - Example programs. For testing
LEDS = [0x303, 0x1FB, 0xE00, 0x00E]
SEC1 = [0x307, 0x1FB, 0xF00, 0x308, 0x1FB, 0xF00, 0x700, 0x009, 0x006]
SEC2 = [0x307, 0x1FB, 0xF00, 0x308, 0x1FB, 0xF00, 0x700, 0x00C, 0x003]

# -- Byte that is received when the bootloader is ready
BREADY = b'B'


# -- Download the program
def download(ser, prog):

    tam = len(prog)
    print("Size: {} byte(s)".format(tam))

    # -- Send program size (in words)
    tamb = tam.to_bytes(2, byteorder='big')
    ser.write(tamb)

    # -- Transmit the program
    for inst in prog:

        # -- Convert the word to bytes
        instb = inst.to_bytes(2, byteorder='big')

        # -- Send the bytes
        ser.write(instb)


# -- Main program
if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB1', baudrate=115200, timeout=0.5)

    # -- Reset Simplez
    ser.setDTR(1)
    time.sleep(0.2)
    ser.setDTR(0)

    # -- Wait for the character "B" to be received. It means the bootloader is ready
    if ser.read() == BREADY:
        print("Bootloader ready!!!!")
    else:
        print("ERROR: NO bootloader")

    # download(ser, LEDS)
    # download(ser, SEC2)
    download(ser, SEC1)

    print("EXECUTING!!!")
