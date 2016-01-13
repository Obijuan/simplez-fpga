; Programa de ejemplo para Simplez
; EJEMPLO 4: Intercambio de dos zonas de memoria: (Bloque 100-150 con bloque 200-250)
; El primer dato de la zona 1 es 0. Al finalizar el intercambio habrá una F en este dato
; Se saca por los leds para comprobar


        BR /ini
k50     DATA 50
k1      DATA 1
cont    DATA 0
tmp     DATA 0

ini     LD /k50   ; Inicializacion del contador
        ST /cont
inst1   LD /200   ; LLeva palabra de zona 2
        ST /tmp   ; a memoria intermedia
inst2   LD /zona1   ; Lleva palabra de zona 1 a
inst3   ST /zona2   ; zona 2
        LD /tmp     ; Lleva memoria intermedia
inst4   ST /zona1   ; a zona 1
        LD /cont
        DEC       ; Decrementar contador
        BZ /fin   ; Si ha llegado a cero, fin
        ST /cont    ; si no, lo actualiza
        LD /inst1   ; Modificacion
        ADD /k1     ; de la
        ST /inst1   ; Instruccion  [7]
        LD /inst2   ; Modificacion
        ADD /k1     ; de la
        ST /inst2   ; Instruccion [9]
        LD /inst3    ; Modificacion
        ADD /k1      ; de la
        ST /inst3    ; instruccion [10]
        LD /inst4    ; modificacion
        ADD /k1      ; de la
        ST /inst4    ; instruccion 12
        BR /inst1    ; Vuelta al bucle

fin     LD /zona1   ;-- Comprobar lo que hay en la posicion 100 sacandolo por los leds
        ST /leds
        HALT

        ;-- Zona de memoria 1
        org 100
zona1   DATA 0
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

zona2   DATA H'F

;---- Perifericos

      ORG 507
leds  RES 1    ;-- Leds. Reservar 1 posicion de memoria en la direccion 507

     end
