#!/usr/bin/python3
# ------------------------------------------------------------------------------
# -  Cargador de programas en SIMPLEZ
# --  (C) BQ Enero 2016. Written by Juan Gonzalez (obijuan)
# --  Python 3
# ------------------------------------------------------------------------------
# - La FPGA tiene que estar configurada con SIMPLEZ con el programa boot.asm
# grabado (es un bootloader).
# - sboot.py se comunica con el bootloader
# - Al arrancar SIMPLEZ se ejecuta el bootloader. El protocolo es el siguiente:
# -
# -  Bootloader: Envía el caracter BREADY para indicar que esta listo
# -  sboot envía primero el tamaño del fichero a cargar, en palabras
# -  Cada palabra se envía como 2 bytes, primero el de mayor peso y luego
# -  el de menor
# -  A continuación sboot comienza a enviar todas las palabras que componen
# - el programa
# -  Cuando se han enviado todas, el bootloader le pasa el control al nuevo
# - programa cargado
# ------------------------------------------------------------------------------
# - Los programas a cargar tiene que comenzar a patir de la direccion 40h
# ------------------------------------------------------------------------------

import serial
import time
import sys
import vmem
import consola_io
import threading


# -- Character for quiting the interactive mode
EXITCHAR = b'\x04'

# - Example programs. For testing
LEDS = [0x303, 0x1FB, 0xE00, 0x00E]
SEC1 = [0x307, 0x1FB, 0xF00, 0x308, 0x1FB, 0xF00, 0x700, 0x009, 0x006]
SEC2 = [0x307, 0x1FB, 0xF00, 0x308, 0x1FB, 0xF00, 0x700, 0x00C, 0x003]

# -- Byte that is received when the bootloader is ready
BREADY = b'B'

# -- Initial address were the programs are loaded
INITIAL_ADDR = 0x40

# -- Flag for indicating that the threads are executing
executing = 1


# -- Download the program
def download(ser, prog):

    tam = len(prog)

    # -- Send program size (in words)
    tamb = tam.to_bytes(2, byteorder='big')
    ser.write(tamb)

    # -- Transmit the program
    for inst in prog:

        # -- Convert the word to bytes
        instb = inst.to_bytes(2, byteorder='big')

        # -- Send the bytes
        ser.write(instb)


def reader(ser):
    """Thread for reading data from simplez and printing on the screen"""
    while executing:
        try:
            data = ser.read()
        except:
            print("Serial reading error")
            sys.exit(0)

        try:
            sys.stdout.write(data.decode("utf-8"))
            sys.stdout.flush()
        except:
            pass


def parse_file(filename):
    """Parse the file with the machine code. It returns:
    (Initial address and memory block)"""

    # -- Read the file
    try:
        with open(filename, mode='r') as f:
            rawdata = f.read()
    except:
        print("Error: file not found: {}".format(filename))
        sys.exit()

    # Create the lexer with some data
    l = vmem.Lexer(rawdata)

    # -- Read the first block
    init_addr, bmem = l.get_block()

    # -- Return the size, initial addr and memory block
    return init_addr, bmem


def parse_arguments():
    """Parse the arguments"""

    import argparse
    description = \
        """SIMPLEZ Loader.  Load programs into the simplez RAM memory"""

    # -- Add the description
    parser = argparse.ArgumentParser(description=description)

    # -- Add the assembler input file
    parser.add_argument("inputfile", help="Simplez machine code file (.list)")

    parser.add_argument("-t", help="Load a test example (-t 1)",
                        action="store_true")

    parser.add_argument(
        "-i",
        help="Open an interactive serial terminal for comunicating with Simplez",
        action="store_true")

    # -- Parse the anguments
    args = parser.parse_args()

    # -- Return the input file, test and interactive
    return args.inputfile, args.t, args.i


def main():

    # -- Process the arguments
    input_file, test, interactive = parse_arguments()

    if test:
        # -- Load the test example
        print("Test!")
        prog = [0x24D, 0x1FB, 0xF00, 0x24E, 0x1FB, 0xF00, 0x24F, 0x1FB, 0xF00,
                0x250, 0x1FB, 0xF00, 0x640, 0x001, 0x002, 0x004, 0x008]
    else:
        # -- Load from file
        # -- Parse the input file. Format: verilog memory. Data is hexadecimal
        init_addr, prog = parse_file(input_file)

        print("File: {}".format(input_file))
        print("Size: {} words".format(len(prog)))
        print("Initial address: H'{:03X}".format(init_addr))

        if init_addr < INITIAL_ADDR:
            print("Error: Initial address below H'{:03X}".format(INITIAL_ADDR))
            sys.exit(0)

        if init_addr > INITIAL_ADDR:
            print("Warning: Initial address is NOT H'{:03X}".format(
                   INITIAL_ADDR))

    ser = serial.Serial('/dev/ttyUSB1', baudrate=115200, timeout=0.5)

    # -- Reset Simplez
    ser.setDTR(1)
    time.sleep(0.2)
    ser.setDTR(0)

    # -- Wait for the character "B" to be received. It means the bootloader
    # --  is ready
    if ser.read() == BREADY:
        print("Bootloader ready!!!!")
    else:
        print("ERROR: NO bootloader")
        sys.exit(0)

    # download(ser, LEDS)
    # download(ser, SEC2)
    download(ser, prog)

    print("EXECUTING!!!")

    # -- If in interactive mode (-i option), a simple terminal is created
    if interactive:
        print("Entering the interactive mode...")
        print("Press CTRL-D to exit\n")

        # -- Launch a thread for reading the data coming from simplez
        r = threading.Thread(target=reader, args=[ser])
        r.start()

        # -- Sending data to simplez from the keyboard
        while 1:
            try:
                # -- Wait for a key typed
                c = consola_io.getkey()

                # -- Exit char
                if c == EXITCHAR:
                    break
                else:
                    # -- Send the char to simplez
                    ser.write(c)

            except:  # -- Si se ha pulsado control-c terminar
                print ("Abortando...")
                break

        global executing
        executing = 0
        r.join()

    ser.close()

# -- Main program
if __name__ == '__main__':
    main()
