;-------------------------------------------------------------------------------------------
;-- Programa de ejemplo para Bootloader.
;-- Contador de 4 bits por los leds
;--
;-- Este programa se carga mediante el bootloader
;--------------------------------------------------------------------------------------------

;-- Acceso a los perifericos
leds    EQU 507

;-- Comienzo del programa:
;-- Direccion h'40: para cargarlo con el bootloader
        org h'40

       ld /val1   ; Inicializar acumulador
       st /leds   ; Mostrarlo por los leds
bucle  WAIT
       add /uno   ; Incrementar en uno
       st /leds   ; Sacarlo por los leds
       BR /bucle   ; Repetir

;--- Datos
val1    DATA  h'1
uno     DATA  h'1

     end
