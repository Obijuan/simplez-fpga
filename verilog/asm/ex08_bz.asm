;-- Programas de prueba para Simplez
;-- Ejemplo 8: Prueba de BZ.  Se comprueba el valor de comp
;--  Si comp == 0: LEDS = 1 (Se enciende un led)
;--  Si comp != 0: LEDS = F (se encienden todos los leds)
;-- Cambiar el valor de comp para comprobarlo

       WAIT         ;-- Inicio: esperar 200ms

       ld /comp     ; Valor a comparar
       bz /iscero

       ;-- El valor NO es cero
       ld /valn0
       st /leds    ;-- Sacar valn0 por los leds
       HALT

;-- El valor es cero
iscero ld /val0
       st /leds    ;-- Sacar val0 por los leds
       HALT

;--- Datos
comp    DATA  0     ;-- Valor a comparar. Poner 0 o un numero distinto de cero
val0    DATA  h'1   ;-- Valor cuando A es 0
valn0   DATA  h'F   ;-- Valor cuando A NO es 0

;---- Perifericos

      ORG 507
leds  RES 1    ;-- Leds. Reservar 1 posicion de memoria en la direccion 507

     end
