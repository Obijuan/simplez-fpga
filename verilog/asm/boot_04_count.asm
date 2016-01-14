;-- Programas de prueba para Simplez
;-- Ejemplo 7: Contador por los leds
;-- Se incrementa el acumulador de uno en uno, y se saca por los leds


       org h'100

       wait       ;-- Inicio: esperar 200ms

       ld /val1   ; Inicializar acumulador
       st /leds   ; Mostrarlo por los leds
bucle  WAIT
       add /uno   ; Incrementar en uno
       st /leds   ; Sacarlo por los leds
       BR /bucle   ; Repetir

;--- Datos
val1    DATA  h'1
uno     DATA  h'1


;---- Perifericos

      ORG 507
leds  RES 1    ;-- Leds. Reservar 1 posicion de memoria en la direccion 507

     end
