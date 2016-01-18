;-------------------------------------------------------------------------------------------
;-- Programa de ejemplo para Bootloader. Secuencia desplazamiento de un led que se saca
;-- por los leds
;--
;-- Este programa se carga mediante el bootloader
;--------------------------------------------------------------------------------------------

;-- Acceso a los perifericos
leds    EQU 507

;-- Comienzo del programa:
;-- Direccion h'40: para cargarlo con el bootloader
        org h'40

loop    LD /val1
        ST /leds
        Wait
        ld /val2
        st /leds
        wait
        LD /val4
        ST /leds
        Wait
        ld /val8
        st /leds
        wait
        BR /loop

val1     DATA h'1
val2     DATA h'2
val4     DATA h'4
val8     DATA h'8

END
