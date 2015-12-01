; Programa de ejemplo para Simplez
; EJEMPLO 1: Suma de dos numeros
; Version CON ETIQUETAS

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

        ld /num1
        add /num2
        st /suma
        HALT

num1    DATA H'7
num2    DATA H'8
suma    DATA 0
