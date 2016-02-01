#! /usr/bin/python3
# ---------------------------------------------------------------------------
# --  (C)2002-2004 Chris Liechti <cliecht@gmx.net>
# --  (C) 2007 Juan Gonzalez
# --  (C) 2016 Juan Gonzalez
# --
# --  Modulo para trabajar con el teclado de la consola sin tener que
# --  "apretar" enter. Es multiplataforma, para Linux y Windows
# --
# --  LICENCIA GPL
# ---------------------------------------------------------------------------

import os

# -- Seleccionar la plataforma

# -- Windows
if os.name == 'nt':
    import msvcrt

    def getkey():
        while 1:
            z = msvcrt.getch()
            if z == '\0' or z == '\xe0':    # functions keys
                msvcrt.getch()
            else:
                if z == '\r':
                    return '\n'
                return z

# -- Sistemas Posix
elif os.name == 'posix':

    import termios
    import sys
    import atexit

    # -- Abrir la consola y modificar sus propiedades
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    new = termios.tcgetattr(fd)
    new[3] = new[3] & ~termios.ICANON & ~termios.ECHO
    new[6][termios.VMIN] = 1
    new[6][termios.VTIME] = 0

    # -- Cambiar los atributos
    termios.tcsetattr(fd, termios.TCSANOW, new)

    # -- Funcion para leer una tecla
    def getkey():
        c = os.read(fd, 1)
        return c

    # -- Funcion para restablecer la consola al finalizar
    def cleanup_console():
        termios.tcsetattr(fd, termios.TCSAFLUSH, old)

    # -- Restaurar el terminal a la salida
    atexit.register(cleanup_console)

else:
    raise "Consola_io No esta implementado para la plataforma".format(sys.platform)

# -------------------------------------
# Pequena prueba del modulo
# -------------------------------------
if __name__ == '__main__':

    print ("Pulse una tecla")
    getkey()
    print ("Adios...")
