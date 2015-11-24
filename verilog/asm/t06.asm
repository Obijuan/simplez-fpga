;-- Programas de prueba para Simplez
;-- t0.asm: Pruebas de store


;---------------------------------------------------------------------------------
; NOTA: En yosys/icestorm hay un bug que hace que el contenido de la
; posicion 0 de la RAM se ponga a 0 esporádicamente al arrancar
; Por ello la primera instruccion se debe ignorar. El programa debe empezar
; en la direccion 1
;
; $ yosys -V
; Yosys 0.5+397 (git sha1 c86fbae, clang 3.6.2-1 -fPIC -Os)
;---------------------------------------------------------------------------------
NOP  DATA 0    ;-- Ignorar esta intruccion

;-- El programa comienza aqui

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
