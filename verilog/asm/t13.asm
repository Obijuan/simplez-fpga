;-- Programas de prueba para Simplez
;-- t12.asm: Prueba 2 de DEC


       ld /valini     ; Valor inicial cuenta atras
loop
       wait
       DEC
       BR /loop
       HALT

;--- Datos
valini    DATA  h'F