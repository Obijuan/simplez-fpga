; Programa de ejemplo para Simplez
; EJEMPLO 2: Suma de los diez primeros terminos de la sucesion de Fibonacci
; 1 + 1 + 2 + 3 +5 + 8 + 13  + 21 + 34 = 88
; La suma en hexa es 0x58. Por los leds debe salir el valor 8 (1 led encendido)
; Version CON ETIQUETAS


        CLR
        ST /pen   ; PEN = 0
        LD /uno
        ST /ult   ; ULT = 1
        ST /sum   ; SUM = 1
        LD /ocho
        ST /cont  ; CONT = 8

loop    LD /pen
        ADD /ult
        ST /sig    ; SIG = PEN + ULT
        ADD /sum   ; SIG+NUM
        ST /sum    ; SUM = SIG + NUM
        LD /ult
        ST /pen    ; PEN = ULT
        LD /sig
        ST /ult    ; ULT = SIG
        LD /cont   ; CONT
        DEC        ; CONT--
        BZ  /fin   ; si es cero, sale del bucle
        ST /cont   ; si no, lo lleva a CONT
        BR /loop   ; y vuelve al bucle

;-- Fin. Cargar la suma en registro A para mostrarlo por los leds
fin     LD /sum
        st /leds
        HALT


        ;-- Variables
        ORG 46
cont    DATA 0
pen     DATA 0
ult     DATA 0
sig     DATA 0
sum     DATA 0
uno     DATA 1
ocho    DATA 8

;---- Perifericos

      ORG 507
leds  RES 1    ;-- Leds. Reservar 1 posicion de memoria en la direccion 507

     end
