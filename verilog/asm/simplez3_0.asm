; Programa de ejemplo para Simplez
; EJEMPLO 3: Suma de cien números almacenados en la memoria (desde la 100 a la 149)

; ATENCION: Al ejecutarlo en el simplez sintetizado, solo funcionara la primera vez,
; haciendo la suma correcta. Sin embargo las siguientes veces, hará sumas distintas
; porque es un programa que se modifica a si mismo

; Para que siempre se ejecute igual, hay que modificar el programa para que se almacene
; la instruccion ADD /149 en la posicion 6
;  (No se ha hecho para respetar el programa original de Gregorio Fernandez)


        BR /3
        DATA 100    ; Constante 100
        DATA 0      ; Reservada para contar
        LD /1
        ST /2       ; Inicial el contador
        CLR
        ADD /149    ; Suma los numeros
        ST  /150    ; Resultados parciales
        LD /2
        DEC
        BZ /17      ; Si es cero fin
        ST /2       ; si no, actualizarlo
        LD /6       ; modificacion
        DEC         ; de la
        ST /6       ; Instruccion 6
        LD /150     ; Carga ultimo resultado parcial
        BR /6       ; Vuelta al bucle

        ;-- fin
        ;-- Cargar el resultado final en el acumulador A para verlo en los leds
        LD /150
        HALT

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

        org 150
        DATA 0    ; Suma
