;-- Programas de prueba para Simplez
;-- t11.asm: Prueba 1 de BZ


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
