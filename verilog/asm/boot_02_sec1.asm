;-------------------------------------------------------------------------------------------
;-- Programa de ejemplo para Bootloader. Secuencia de dos estados que se saca por los leds
;--
;-- Este programa se carga mediante el bootloader
;--------------------------------------------------------------------------------------------

;-- Acceso a los perifericos
leds    EQU 507

;-- Comienzo del programa:
;-- Direccion h'40: para cargarlo con el bootloader
        org h'40


loop    LD /val1    ;-- Valor secuencia 1
        ST /leds
        Wait
        ld /val2    ;-- Valor secuencia 2
        st /leds
        wait
        BR /loop

val1     DATA h'9
val2     DATA h'6

END
