;-- Programas de prueba para Simplez
;-- t0.asm: Pruebas de store


ini  ld /val1   ; Almacenar val1 en val2
     st /val2
     wait
     wait
     ld /cero   ; Poner a cero A
     wait
     wait
     wait
     wait
     ld /val2   ; Cargar val2. Debe ser igual a val 1
     wait
     HALT


;--- Datos
val1    DATA  h'5
val2    DATA  h'0
cero    DATA  h'0
