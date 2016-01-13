;-- Bootloader para Simplez

INI     EQU  h'100  ;-- Direccion de inicio de carga del programa

        Wait      ;-- Inicio: esperar 200ms

        LD /F     ;-- Encender todos los leds para indicar modo bootloader
        ST /LEDS

        LD /DESTC  ;-- Inicializar la direccion destino, donde cargar el programa
        ST /dest

;-- Enviar caracter "B" para indicar que bootloader listo
txloop  LD /TXSTATUS  ;-- Esperar a que pantalla lista
        BZ /txloop
        LD /B
        ST /TXDATA

;--- Esperar a recibir el programa. Primero se recibe el numero de bytes
;-- La palabra es de 2 bytes. Primero se envia el MAS SIGNIFICATIVO y luego el menor
rxl1   LD /RXSTATUS
       BZ /rxl1

       ;-- Leer caracter
       LD /RXDATA

       ;-- Alcacenar caracter recibido
       ST /tamh

       ;-- Multiplicar por 256 para desplazarlo 8 bits a la izquierda
       ADD /tamh   ; A = tamh + tamh = 2 * tamh. Desplazamiento de un bit a la izquierda
       ST  /tamh
       ADD /tamh   ; A = A + A = 4 * tamh   (2 bits)
       ST /tamh
       ADD /tamh   ; A = A + A = 8 * tamh   (3 bits)
       ST /tamh
       ADD /tamh   ; 16 * tamh (4 bits)
       ST /tamh
       ADD /tamh   ; <-- 5 bits
       ST /tamh
       ADD /tamh   ; <-- 6 bits
       ST /tamh
       ADD /tamh   ; <-- 7 bits
       ST /tamh
       ADD /tamh   ; <-- 8 bits
       ST /tamh

       ;-- Leer la palabra menos significativa
rxl2   LD /RXSTATUS
       BZ /rxl2

       ;-- Leer caracter  (taml)
       LD /RXDATA

       ADD /tamh
       ST /tam     ;--  tam = 256 * tamh + taml

       ST /LEDS    ;-- Debug: visualizar en los leds

       ;-- Bucle principal. Se esperan recibir tam palabras (de 2 bytes)
       ;-- que se almacenaran a partir de la direccion INI

;--------------------------- Main loop
       ;-- Leer byte alto
rxl3   LD /RXSTATUS
       BZ /rxl3

      ;-- Leer caracter
      LD /RXDATA

      ;-- Almacenar caracter recibido
      ST /insth

      ADD /insth  ; <-- (1 bit)
      ST /insth
      ADD /insth  ; <-- (2 bit)
      ST /insth
      ADD /insth  ; <-- (3 bit)
      ST /insth
      ADD /insth  ; <-- (4 bit)
      ST /insth
      ADD /insth  ; <-- (5 bit)
      ST /insth
      ADD /insth  ; <-- (6 bit)
      ST /insth
      ADD /insth  ; <-- (7 bit)
      ST /insth
      ADD /insth  ; <-- (8 bit)
      ST /insth

      ST /LEDS

      ;-- Leer byte bajo
rxl4  LD /RXSTATUS
      BZ /rxl4

      ;-- Leer caracter  (instl)
      LD /RXDATA

      ADD /insth
      ST /inst     ;--  inst = 256 * inst + instl

      ST /LEDS     ;-- Debug

      ;-- Esta instruccion se modifica para almacenar la instrucciones recibida en la
      ;-- siguiente posicion de memoria
dest  ST /INI      ;-- Almacenar la instruccion

      LD  /tam
      DEC           ;-- Un byte menos por recibir
      BZ /fin       ;-- Fin de la carga

      ST /tam      ;-- Actualizar bytes restantes

      ;-- Incrementar la direccion de destino
      LD /dest
      ADD /UNO
      ST /dest     ;-- [dest] = [dest] + 1

      BR /rxl3     ;-- Siguiente palabra

fin    BR /INI     ;-- Ejecutar el programa!


F       DATA h'0f   ;-- Dato a sacar por los leds al comenzar el bootloader
B       DATA "B"    ;-- Caracter para indicar bootloader listo
tam     RES 1       ;-- Tamaño del programa a cargar
tamh    RES 1       ;-- Byte alto del tamaño
insth   RES 1       ;-- Byte alto instruccion
inst    RES 1       ;-- Instruccion
DESTC   ST /INI     ;-- Inicializacion de la direccion destino
UNO     DATA 1      ;-- Constante 1. Para incrementar

;------ PERIFERICOS ------------------

          ORG 507
;-- LEDS
LEDS      DATA    0  ;-- 507: Escritura en leds


;--- PANTALLA
TXSTATUS  DATA    0  ;-- 508:  Registro de estado
TXDATA    DATA    0  ;-- 509:  Registro de datos

;-- Direcciones de acceso al teclado
RXSTATUS  DATA    0  ;-- 510:  Registro de estado
RXDATA    DATA    0  ;-- 511:  Registro de datos

end
