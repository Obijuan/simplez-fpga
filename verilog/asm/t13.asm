;-- Programas de prueba para Simplez
;-- t12.asm: Prueba 2 de DEC


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


       ld /valini     ; Valor inicial cuenta atras
loop
       wait
       DEC
       BR /loop
       HALT

;--- Datos
valini    DATA  h'F
