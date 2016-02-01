;-- Programas de prueba para Simplez
;-- Ejemplo 4: Encender y apagar los leds. Prueba de WAIT
;-- La instruccion wait realiza una pausa de 200ms
;-- se pueden ejecutar varias instrucciones WAIT seguidas para hacer pausas multiplos de 200ms

ini  LD /val1
     ST /leds    ;-- Mostrar valor 1 por los leds

     WAIT        ;-- Espera de 200ms

     LD /val2    ;-- Mostrar valor 2 por los leds
     ST /leds

     WAIT        ;-- Espera de 200ms

     BR /ini


;--- Datos
val1    DATA  h'9
val2    DATA  h'6


;---- Perifericos

      ORG 507
leds  RES 1    ;-- Leds. Reservar 1 posicion de memoria en la direccion 507

     end
