;-- Programas de prueba para Simplez
;-- t16.asm: Prueba de lectura del registro de estado del teclado
;-- Los leds estan apagados (salvo un destello inicial). Cuando se recibe un caracter por
;-- el terminal, se enciende el led 1 (indicando que el registro de estado del teclado
;-- esta a 1)


       ld /val1
       WAIT
loop
       ld /RXSTATUS    ;-- Leer el registro de datos del teclado
       BR /loop
       HALT

val1   DATA H'FF

;-- Direcciones de acceso al teclado

          ORG 510
RXSTATUS  DATA    0  ;-- 510:  Registro de estado
RXDATA    DATA    0  ;-- 511:  Registro de datos
