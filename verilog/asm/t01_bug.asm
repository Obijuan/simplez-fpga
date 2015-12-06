;-- Programas de prueba para Simplez
;-- t01.asm: HALT

;---------------------------------------------------------------------------------
; NOTA: En yosys/icestorm hay un bug que hace que el contenido de la
; posicion 0 de la RAM se ponga a 0 esporádicamente al arrancar
; Por ello la primera instruccion se debe ignorar. El programa debe empezar
; en la direccion 1
;
; $ yosys -V
; Yosys 0.5+397 (git sha1 c86fbae, clang 3.6.2-1 -fPIC -Os)
;
; NOTA: A parir de la version:
; Yosys 0.5+408 (git sha1 1ea6db3, clang 3.6.2-1 -fPIC -Os)
; parece que el bug esta solucionado y no hace falta meter la instruccion NOP en la
; direccion 0
;---------------------------------------------------------------------------------
NOP  DATA 0    ;-- Ignorar esta intruccion

;--- Comienzo del programa

end  HALT  ;-- Terminar
