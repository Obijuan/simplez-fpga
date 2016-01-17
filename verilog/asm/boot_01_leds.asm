;---------------------------------------------------------------------------------
;-- Programa de ejemplo. Sacar un valor por los leds
;--
;-- Este programa se carga mediante el bootloader

;-- Acceso a perifericos
LEDS    EQU 507


;-- Comienzo del programa:
;-- Direccion h'40: para cargarlo con el bootloader
        org h'40

        LD /val
        ST /LEDS
        HALT

val     DATA h'7

END
