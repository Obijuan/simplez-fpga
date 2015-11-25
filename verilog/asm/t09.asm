;-- Programas de prueba para Simplez
;-- t09.asm: Prueba 1 de CLR


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

       ld /val1   ; Inicializar acumulador
       WAIT
       CLR
       HALT

;--- Datos
val1    DATA  h'F
