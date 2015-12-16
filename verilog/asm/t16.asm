;-- Programas de prueba para Simplez
;-- t16.asm: Prueba de lectura del registro de datos del teclado


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
