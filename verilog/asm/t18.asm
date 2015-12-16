;-- Programas de prueba para Simplez
;-- t18.asm: Prueba de puesta a 0 del flag de dato recibido


       ld /val1
       WAIT
loop
       ld /RXSTATUS    ;-- Esperar a que llegue un caracter
       BZ /loop

       ld /RXDATA     ;-- Leer el dato recibido
       WAIT
       WAIT
       WAIT
       WAIT

loop2
       ld /RXSTATUS    ;-- Esperar a que llegue otro caracter
       BZ /loop2

       ld /RXDATA
       HALT

val1   DATA H'FF
val2   DATA H'55

;-- Direcciones de acceso al teclado

          ORG 510
RXSTATUS  DATA    0  ;-- 510:  Registro de estado
RXDATA    DATA    0  ;-- 511:  Registro de datos
