;-- Programas de prueba para Simplez
;-- t15.asm: Prueba de escritura en la pantalla usando el registro de
;--   estado de la pantalla


       ld /val1        ;-- Encender todos los leds
       WAIT            ;-- Y esperar a que todo esté correctamente incializado

;-------- Envio de "H"
wait1
       ld /TXSTATUS    ;-- Leer el registro de estado de la pantalla
       BZ /wait1       ;-- Esperar a que se ponga a 1

       ld /car_H       ;-- Enviar el caracter "H"
       st /TXDATA      ;-- Escribiendo en el registro de datos


;------- Envio de "O"
wait2
       ld /TXSTATUS    ;-- Lo mismo que en el bloque anterior
       BZ /wait2       ;-- Pero con el siguiente caracter

       ld /car_O
       st /TXDATA

;------- Envio de "L"
wait3
       ld /TXSTATUS
       BZ /wait3

       ld /car_L
       st /TXDATA

;------- Envio de "A"
wait4
       ld /TXSTATUS
       BZ /wait4

       ld /car_A
       st /TXDATA

;------- Envio de " "
wait5
       ld /TXSTATUS
       BZ /wait5

       ld /car_sp
       st /TXDATA

       ;-- Terminar el programa
       HALT

val1    DATA H'F
car_H   DATA  h'48   ;-- "H"
car_O   DATA  h'4F   ;-- "O"
car_L   DATA  h'4C   ;-- "L"
car_A   DATA  h'41   ;-- "A"
car_sp  DATA  h'20   ;-- " "


;-- Direcciones de acceso a la pantalla

          ORG 508
TXSTATUS  DATA    0  ;-- 508:  Registro de estado
TXDATA    DATA    0  ;-- 509:  Registro de datos
