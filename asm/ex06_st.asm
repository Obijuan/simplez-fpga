;-- Programas de prueba para Simplez
;-- Ejemplo 6: Prueba de ST. Se lleva el contenido de la variable val1 a la val2 y luego
;-- se saca por los leds, para comprobar que la instruccion de store funciona correctamente

     clr        ;-- Borrar A. No es necesario
     ld /val1   ; Almacenar val1 en val2
     st /val2
     clr
     ld /val2   ; Cargar val2. Debe ser igual a val 1
     st /leds
     HALT


;--- Datos
val1    DATA  h'5
val2    DATA  h'0


;---- Perifericos

      ORG 507
leds  RES 1    ;-- Leds. Reservar 1 posicion de memoria en la direccion 507

     end
