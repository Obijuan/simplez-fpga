;-- Programas de prueba para Simplez
;-- t05.asm: Prueba de saltos y etiquetas


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

ini000  BR /ini1


        org h'10
ini1
        LD /val1
        WAIT
        BR /ini2

        org h'20
ini2    LD /val2
        WAIT
        br /ini3

        org h'30
ini3    LD /val3
        WAIT
        br /ini4

        org h'40
ini4    LD /val4
        WAIT
        br /ini5

        org h'50
ini5    LD /val5
        WAIT
        br /ini6

        org h'60
ini6
        LD /val6
        WAIT
        br /ini7

        org h'70
ini7    LD /val7
        wait
        br /ini8

        org h'80
ini8
        ld /val8
        Wait

        BR /ini000        ;-- Vuelta al comienzo


;--- Datos
val1    DATA  h'1
val2    DATA  h'3
val3    DATA  h'2
val4    DATA  h'6
val5    DATA  h'4
val6    DATA  h'C
val7    DATA  h'8
val8    DATA  h'9
