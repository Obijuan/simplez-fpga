;-- Programas de prueba para Simplez
;-- t10.asm: Prueba 2 de CLR


ini
       ld /val1   ; Inicializar acumulador
       WAIT
       CLR
       WAIT
       BR /ini

;--- Datos
val1    DATA  h'F
