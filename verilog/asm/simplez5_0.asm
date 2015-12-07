; Programa de ejemplo para Simplez
; EJEMPLO 5: Subrutina. Resta de dos numeros



        BR /inicio
        DATA 0      ; -- No usado (puesto para respetar codigo del libro)
        DATA 0
        DATA 0

        BR /0       ; Para construir BR
        DATA 17     ; Direccion de retorno 1
        DATA 27     ; Direccion de retorno 2

        org 10
inicio
        LD /51      ; Transmision del
        ST /202     ;   del sustraendo
        LD /4       ; Construccion de la
        ADD /5      ;   Instruccion
        ST /212     ;   de retorno
        LD /50      ; Transmision del minuendo
        BR /200     ; Salto a subprograma
        ST /52      ; Guardar resultado
        BR /op2

        org 20
op2
        LD /101     ; Transmision del
        ST /202     ;    sustraendo
        LD /4       ; Construccion de la
        ADD /6      ;   Instruccion
        ST /212     ;  de retorno
        LD /52     ; Transmision del minuendo  (Diferente al prog. del libro de Gregorio)
        BR /200     ; Salto al subprograma
        ST /102     ; Guardar resultado
        HALT

        ;--Variables
        org 50
        DATA 15
        DATA 2
        DATA 0

        org 100
        DATA 0
        DATA 1    ; Resta 2
        DATA 0


        org 200
        BR /203   ;-- Comienzo Subprograma
        DATA 0    ;-- Resultado parcial
        DATA 0    ;-- Valor a restar
        DEC       ;-- Decremento del
        ST /201   ;--   resultado parcial
        LD /202   ;-- Decremento del
        DEC       ;--   sustraendo
        BZ /211   ;-- Si ha llegado a cero, fin
        ST /202   ; si no, se actualiza
        LD /201   ;  se carga resultado parcial
        BR /203   ;  y se vuelve al bucle
        LD /201   ; Resultado al acumulador
        DATA 0    ; Aqui deposita el programa la instruccion de retorno
