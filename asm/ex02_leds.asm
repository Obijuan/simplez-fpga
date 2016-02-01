;-- Programas de prueba para Simplez
;-- Ejemplo 2: Sacar un valor por los leds
;-- Los 4 leds se encuentran en la posicion 507 de la memoria
;-- Cualquier escritura en esa direccion hace que los 4 bits menos significativos
;-- del valor escrito se visualicen por los leds

     LD /val     ;-- Cargar en A el valor a sacar por los leds
     ST /leds    ;-- Sacar el valor por los leds
     HALT


;--- Datos
val    DATA  h'F  ;-- Valor que se visualizara en los leds


;---- Perifericos

      ORG 507
leds  RES 1    ;-- Leds. Reservar 1 posicion de memoria en la direccion 507

     end
