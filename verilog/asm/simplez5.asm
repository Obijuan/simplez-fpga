; Programa de ejemplo para Simplez
; EJEMPLO 5: Subrutina. Resta de dos numeros
; Se realiza la resta: result2 = dato - res1 - res2
; Con los valores por defecto, el resultado es 12 (0xC) que se saca por los leds
; VERSION CON ETIQUETAS


        BR /inicio
        DATA 0      ; -- No usado (puesto para respetar codigo del libro)
        DATA 0
        DATA 0

ibr     BR /0       ; Para construir BR
ret1    DATA 17     ; Direccion de retorno 1
ret2    DATA 27     ; Direccion de retorno 2

        org 10
inicio  LD /res1    ; Transmision del
        ST /arg     ;   del sustraendo
        LD /ibr     ; Construccion de la
        ADD /ret1   ;   Instruccion
        ST /return  ;   de retorno
        LD /dato    ; Transmision del minuendo
        BR /restar  ; Salto a subprograma
        ST /result1 ; Guardar resultado
        BR /op2

        org 20
op2     LD /res2      ; Transmision del
        ST /arg       ;    sustraendo
        LD /ibr       ; Construccion de la
        ADD /ret2     ;   Instruccion
        ST /return    ;  de retorno
        LD /result1   ; Transmision del minuendo  (Diferente al prog. del libro de Gregorio)
        BR /restar    ; Salto al subprograma
        ST /result2   ; Guardar resultado
        ST /leds
        HALT

        ;--Variables
        org 50
dato    DATA 15
res1    DATA 2
result1 DATA 0

        org 100
        DATA 0
res2    DATA 1    ; Resta 2
result2 DATA 0


        org 200
restar  BR /rini   ;-- Comienzo Subprograma
parc    DATA 0     ;-- Resultado parcial
arg     DATA 0     ;-- Valor a restar

rini    DEC        ;-- Decremento del
        ST /parc   ;--   resultado parcial
        LD /arg    ;-- Decremento del
        DEC        ;--   sustraendo
        BZ /fin    ;-- Si ha llegado a cero, fin
        ST /arg    ; si no, se actualiza
        LD /parc   ;  se carga resultado parcial
        BR /rini   ;  y se vuelve al bucle

fin     LD /parc   ; Resultado al acumulador
return  DATA 0     ; Aqui deposita el programa la instruccion de retorno

;---- Perifericos

      ORG 507
leds  RES 1    ;-- Leds. Reservar 1 posicion de memoria en la direccion 507

     end


end
