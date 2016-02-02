;-- Programas de prueba para Simplez
;-- Ejemplo 3: Encender y apagar los leds. Prueba de WAIT
;-- La instruccion wait realiza una pausa de 200ms
;-- se pueden ejecutar varias instrucciones WAIT seguidas para hacer pausas multiplos de 200ms

     WAIT
     LD /val1
     ST /leds    ;-- Encender los leds

     WAIT        ;-- Espera de 200ms
     ;-- WAIT    ;-- Mas pausa (opcional)

     CLR         ;-- Apagar los leds
     ST /leds

     HALT


;--- Datos
val1    DATA  h'F  ;-- Valor que se visualizara en los leds


;---- Perifericos

      ORG 507
leds  RES 1    ;-- Leds. Reservar 1 posicion de memoria en la direccion 507

     end
