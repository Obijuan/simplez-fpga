;-- Programas de ejemplo para Simplez
;-- sec.asm: Sacar una secuencia de 2 estados por los leds

loop
    LD /val1   ;-- Sacar valor 1 por los leds
    ST /LEDS
    WAIT       ; Pausa
    LD /val2   ;-- Sacar valor 2 por los leds
    ST /LEDS
    WAIT
    BR /loop   ;-- Repetir


;-- Datos
val1  DATA H'03   ;-- Valor 1 de la secuencia
val2  DATA H'0C   ;-- Valor 2 de la secuencia


;------ PERIFERICO: puerto de leds ------------------

          ORG 507

LEDS      DATA    0  ;-- Todo lo escrito aqui se saca por los leds
