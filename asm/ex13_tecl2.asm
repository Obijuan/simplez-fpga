;-- Programas de prueba para Simplez
;-- Ejemplo 13: Lectura del teclado. Todo lo recibido se saca por los leds

       WAIT         ;-- Inicio: esperar 200ms

       ld /val1     ;-- Encender todos los leds para indicar que esta listo para recibir
       st /LEDS
       WAIT

loop   ld /RXSTATUS    ;-- Esperar a que llegue un caracter
       BZ /loop

       ld /RXDATA     ;-- Leer el dato recibido
       st /LEDS       ;-- Sacarlo por los leds
       BR /loop

val1   DATA H'0F      ;--Constante para encender todos los leds

;----------------- PERIFERICOS

          ORG 507
;-- LEDS
LEDS      DATA    0  ;-- 507: Escritura en leds

          ORG 510
;--- Teclado
RXSTATUS  DATA    0  ;-- 510:  Registro de estado
RXDATA    DATA    0  ;-- 511:  Registro de datos

end
