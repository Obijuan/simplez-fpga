
;------------------------------------------------------------------------------
;-- Bootloader para Simplez
;------------------------------------------------------------------------------
;-- (c) 2016-2017. Juan Gonzalez (obijuan)
;-- Licensed under the LGLP v3 License
;------------------------------------------------------------------------------
;-- El protocolo de comunicacion entre el PC y simplez es el siguiente:
;--
;--  Al arrancar, simplez ejecuta este bootloader
;--  Simplez envia el caracter BREADY al PC (transmision serie) para informar
;--  que el bootloader esta listo para recibir un programa
;--
;--  El PC envia el tamaño del programa a cargar, en una palabra de simplez
;-- (12 bits) Se envia dividida en 2 bytes: primero el byte de mayor peso,
;;-- y luego el de menor
;--
;--  A continuacion se envían todas las palabras con los datos / instrucciones
;--  que se almacenan SECUENCIALMENTE a partir de la direccion inicial de carga
;-- (40h) Cada dato es de 12 bits, por lo que se envía en 2 bytes (primero el
;--  alto y luego el bajo)
;------------------------------------------------------------------------------
;-- LOS PROGRAMAS A CARGAR DEBEN EMPEZAR A PARTIR DE LA DIRECCION 40h
;------------------------------------------------------------------------------

;-- Direccion de inicio de carga de los programas
INI     EQU  h'40

;---------------------------------------------------
;-- Constantes para acceso a PERIFERICOS
;---------------------------------------------------
LEDS      EQU  507    ;-- Periferico: LEDS
TXSTATUS  EQU  508    ;-- 508:  Registro de estado pantalla
TXDATA    EQU  509    ;-- 509:  Registro de datos  pantalla
RXSTATUS  EQU  510    ;-- 510:  Registro de estado teclado
RXDATA    EQU  511    ;-- 511:  Registro de datos teclado


            Wait      ;-- Inicio: esperar 200ms

            LD /DESTC  ;-- Inicializar la direccion destino, donde cargar
            ST /dest   ;-- el programa

;-- Enviar caracter "B" para indicar que bootloader listo
txloop      LD /TXSTATUS  ;-- Esperar a que pantalla lista
            BZ /txloop
            LD /BREADY
            ST /TXDATA    ;-- Enviar caracter B

;-- Esperar respuesta del PC. Si no se recibe ningun caracter, se salta
;-- a la direccion donde esta el programa cargado
            wait
            wait
            LD /RXSTATUS
            BZ /INI  ;-- Ningun caracter: ejecutar prog almacenado

            LD /RXDATA ;-- Caracter basura. Ignorar

;--- Leer el tamano del programa, llamando a read_byte()
;---  tam = read_word()
            LD /br_template
            ADD /ret_addr_p1
            ST /br_ret
            BR /read_word
ret_addr1   ST /tam

;-- Bucle de recepcion del programa. Se esperan recibir tam palabras
;-- (de 2 bytes) que se almacenaran a partir de la direccion INI


;--- data = read_word()
prog_loop   LD /br_template
            ADD /ret_addr_p2
            ST /br_ret
            BR /read_word
ret_addr2   ST /inst

      ;-- Esta instruccion se modifica para almacenar la instrucciones
      ;--  recibida en la siguiente posicion de memoria
dest  ST /INI      ;-- Almacenar la instruccion

      LD  /tam
      DEC           ;-- Un byte menos por recibir
      BZ /fin       ;-- Fin de la carga

      ST /tam      ;-- Actualizar bytes restantes

      ;-- Incrementar la direccion de destino
      LD /dest
      ADD /UNO
      ST /dest     ;-- [dest] = [dest] + 1

      BR /prog_loop   ;-- Siguiente palabra

fin    BR /INI     ;-- Ejecutar el programa!


BREADY  DATA "B"    ;-- Caracter para indicar bootloader listo
tam     RES 1       ;-- Tamaño del programa a cargar
inst    RES 1       ;-- Instruccion
DESTC   ST /INI     ;-- Inicializacion de la direccion destino
UNO     DATA 1      ;-- Constante 1. Para incrementar



;------------------------------------------------------------------------------
;-- Subrutina: read_word()
;------------------------------------------------------------------------------
;-- Leer por el puerto serie 2 bytes y convertilos a una palabra
;-- A = byteh * 256 + bytel
;-- Primero se recibe el byte mas significativo (byteh) y luego el menor
;-- (bytel)
;--
;-- DEVUELVE:
;--    -El registro A contiene el valor de vuelta, con la palabra leida
;------------------------------------------------------------------------------

read_word    LD /RXSTATUS
             BZ /read_word

             ;-- Leer caracter
             LD /RXDATA

             ;-- Alcacenar caracter recibido
             ST /byteh

             ;-- Inicializar contador de bits a 8
             LD /k8
             ST /shift_count

             ;-- Multiplicar por 256 para desplazarlo 8 bits a la izquierda
shift_loop   LD /byteh
             ADD /byteh   ; A = byteh + byteh = 2 * byteh. Desplazamiento
             ST  /byteh   ; de un bit a la izquierda
             LD /shift_count
             DEC
             BZ /rxl2
             ST /shift_count
             BR /shift_loop

;-- Leer la palabra menos significativa
rxl2         LD /RXSTATUS
             BZ /rxl2

             ;-- Leer caracter  (taml)
             LD /RXDATA
             ADD /byteh

br_ret       BR /0     ;-- Retorno de subrutina (la instruccion se modifica)

shift_count  RES  1
k8           DATA 8  ;-- Constante 8
br_template  BR /0   ;-- Instruccion BR. Para usarla como ret de las subrutinas
ret_addr_p1  DATA ret_addr1  ;-- Puntero a la direccion ret_addr1
ret_addr_p2  DATA ret_addr2  ;-- Puntero a la direccion ret_addr2
byteh        RES 1           ;-- Byte alto del tamaño


;--- Comienzo del programa cargado. Por defecto no se hace nada
            ORG INI
            halt

end
