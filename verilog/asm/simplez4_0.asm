; Programa de ejemplo para Simplez
; EJEMPLO 4: Intercambio de dos zonas de memoria: (Bloque 100-150 con bloque 200-250)


        BR /5
        DATA 50   ; Constante 50
        DATA 1    ; Constante 1
        DATA 0    ; Reservada para contar memoria intermedia
        DATA 0
        LD /1     ; Inicializacion del contador
        ST /3
        LD /200   ; LLeva palabra de zona 2
        ST /4     ; a memoria intermedia
        LD /100   ; Lleva palabra de zona 1 a
        ST /200   ; zona 2
        LD /4     ; Lleva memoria intermedia
        ST /100   ; a zona 1
        LD /3
        DEC       ; Decrementar contador
        BZ /30    ; Si ha llegado a cero, fin
        ST /3     ; si no, lo actualiza
        LD /7     ; Modificacion
        ADD /2    ; de la
        ST /7     ; Instruccion  [7]
        LD /9     ; Modificacion
        ADD /2    ; de la
        ST /9     ; Instruccion [9]
        LD /10    ; Modificacion
        ADD /2    ; de la
        ST /10    ; instruccion [10]
        LD /12    ; modificacion
        ADD /2    ; de la
        ST /12    ; instruccion 12
        BR /7     ; Vuelta al bucle

        ;-- Comprobar lo que hay en la posicion 100 sacandolo por los leds
        LD /100
        ST /507
        HALT

        ;-- Zona de memoria 1
        org 100
        DATA 0
        DATA 1
        DATA 2
        DATA 3
        DATA 4
        DATA 5
        DATA 6
        DATA 7
        DATA 8
        DATA 9

        DATA 10
        DATA 11
        DATA 12
        DATA 13
        DATA 14
        DATA 15
        DATA 16
        DATA 17
        DATA 18
        DATA 19

        DATA 20
        DATA 21
        DATA 22
        DATA 23
        DATA 24
        DATA 25
        DATA 26
        DATA 27
        DATA 28
        DATA 29

        DATA 30
        DATA 31
        DATA 32
        DATA 33
        DATA 34
        DATA 35
        DATA 36
        DATA 37
        DATA 38
        DATA 39

        DATA 40
        DATA 41
        DATA 42
        DATA 43
        DATA 44
        DATA 45
        DATA 46
        DATA 47
        DATA 48
        DATA 49


        ;-- Zona de memoria 2
        org 200

        DATA H'F

end
