;-- Programas de prueba para Simplez
;-- t03.asm: Pruebas de WAIT


     LD /val1
     WAIT
     LD /val2
     WAIT

     HALT        ;-- Terminar


;--- Datos
val1    DATA  h'9
val2    DATA  h'6
