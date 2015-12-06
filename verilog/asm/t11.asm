;-- Programas de prueba para Simplez
;-- t11.asm: Prueba 1 de BZ


       ld /comp     ; Valor a comparar
       bz /iscero

       ;-- El valor NO es cero
       ld /valn0
       HALT

iscero ;-- El valor es cero
       ld /val0
       HALT

;--- Datos
comp    DATA  h'0   ;-- Colocar un valor 0 o distinto de cero
val0    DATA  h'1   ;-- Valor cuando A es 0
valn0   DATA  h'F   ;-- Valor cuando A NO es 0
