;-- Programas de prueba para Simplez
;-- t17.asm: Prueba de lectura del registro de datos


       ld /val1
       WAIT
loop
       ld /RXSTATUS    ;-- Esperar a que llegue un caracter
       BZ /loop

       ld /RXDATA     ;-- Leer el dato recibido
       HALT

val1   DATA H'FF
val2   DATA H'55

;-- Direcciones de acceso al teclado

          ORG 510
RXSTATUS  DATA    0  ;-- 510:  Registro de estado
RXDATA    DATA    0  ;-- 511:  Registro de datos
