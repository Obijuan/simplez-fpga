;-- Programas de prueba para Simplez
;-- t20.asm: Prueba del periferico de leds: acceso a los leds
;-- Para funcionar correctamente el parametro DEBUG_LEDS tiene que estar a 0


       CLR
       ld /val1
       st /LEDS
       CLR
       HALT

val1   DATA H'FF

;-- Direcciones de acceso a perifericos

          ORG 507
LEDS      DATA    0  ;-- 507:  Puerto de escritura en leds
