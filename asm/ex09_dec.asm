;-- Programas de prueba para Simplez
;-- Ejemplo 9: Prueba de DEC.  Cuenta atrás por los leds

       WAIT         ;-- Inicio: esperar 200ms

       ld /valini     ; Valor inicial cuenta atras
       st /leds
loop   wait
       DEC
       st /leds
       BR /loop

       HALT

;--- Datos
valini    DATA  h'F


;---- Perifericos

      ORG 507
leds  RES 1    ;-- Leds. Reservar 1 posicion de memoria en la direccion 507

     end
