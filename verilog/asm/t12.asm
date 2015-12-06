;-- Programas de prueba para Simplez
;-- t12.asm: Prueba 1 de DEC

       ld /val     ; Valor a decrementar
       wait
       wait
       DEC
       HALT

;--- Datos
val    DATA  h'8
