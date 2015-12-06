;-- Programas de prueba para Simplez
;-- t04.asm: Prueba de BR: Secuencia infinita

ini
     LD /val1
     WAIT
     LD /val2
     WAIT

     BR /ini        ;-- Vuelta al comienzo


;--- Datos
val1    DATA  h'9
val2    DATA  h'6
