; Programa de ejemplo para Simplez
; EJEMPLO 2: Suma de los diez primeros terminos de la sucesion de Fibonacci


        CLR       ; 0
        ST /47    ; a PEN
        LD /51    ; 1
        ST /48    ; a ULT
        ST /50    ; a SUM
        LD /52    ; 8
        ST /46    ; a CONT
        LD /47    ; PEN
        ADD /48   ; PEN+ULT
        ST /49    ; a SIG
        ADD /50   ; SIG+NUM
        ST /50    ; a SUM
        LD /48    ; ULT
        ST /47    ; a PEN
        LD /49    ; SIG
        ST /48    ; a ULT
        LD /46    ; CONT
        DEC       ; Lo decrementa
        BZ  /21   ; si es cero, sale del bucle
        ST /46    ; si no, lo lleva a CONT
        BR /7     ; y vuelve al bucle

        ;-- Fin. Cargar la suma en registro A para mostrarlo por los leds
        LD /50
        HALT


        ;-- Variables
        ORG 46
        DATA 0    ; CONT
        DATA 0    ; PEN
        DATA 0    ; ULT
        DATA 0    ; SIG
        DATA 0    ; SUM
        DATA 1
        DATA 8
