;-- Programas de prueba para Simplez
;-- Ejemplo 5: Secuencia de 8 estados por los leds. Prueba de etiquetas
;-- Se saca una secuencia por los leds. Se hace leyendo directamente los valores de
;-- variables de memoria. Se puede hacer mas optimo, pero el objetivo de este ejemplo
;-- es probar que el ensamblador reconoce bien todas las etiquetas y que cada parte del
;-- codigo se situa en la posicion de memoria indicada

;-- El programa comienza aqui

ini000  BR /ini1  ;--Saltar al primer bloque de codigo


        org h'10
ini1    LD /val1
        ST /leds    ;-- Sacar la variable val1 por los leds
        WAIT        ;-- Esperar
        BR /ini2    ;-- Saltar al siguiente bloque

        org h'20    ;-- Bloque 2: Todos los bloques son iguales
ini2    LD /val2    ;-- Solo cambian las etiquetas
        ST /leds
        WAIT
        br /ini3

        org h'30
ini3    LD /val3
        ST /leds
        WAIT
        br /ini4

        org h'40
ini4    LD /val4
        ST /leds
        WAIT
        br /ini5

        org h'50
ini5    LD /val5
        ST /leds
        WAIT
        br /ini6

        org h'60
ini6    LD /val6
        ST /leds
        WAIT
        br /ini7

        org h'70
ini7    LD /val7
        ST /leds
        wait
        br /ini8

        org h'80
ini8    ld /val8
        ST /leds
        Wait

        BR /ini000        ;-- Vuelta al comienzo


;--- Datos
val1    DATA  h'1
val2    DATA  h'3
val3    DATA  h'2
val4    DATA  h'6
val5    DATA  h'4
val6    DATA  h'C
val7    DATA  h'8
val8    DATA  h'9

;---- Perifericos

      ORG 507
leds  RES 1    ;-- Leds. Reservar 1 posicion de memoria en la direccion 507

     end
