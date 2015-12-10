;-- Programas de prueba para Simplez
;-- t15.asm: Prueba de escritura en la pantalla usando el registro de
;--   estado de la pantalla


       ld /val1
       WAIT

wait1
       ld /TXSTATUS
       BZ /wait1

       ld /car_H
       st /TXDATA

wait2
       ld /TXSTATUS
       BZ /wait2

       ld /car_O
       st /TXDATA

wait3
       ld /TXSTATUS
       BZ /wait3

       ld /car_L
       st /TXDATA

wait4
       ld /TXSTATUS
       BZ /wait4

       ld /car_A
       st /TXDATA

wait5
       ld /TXSTATUS
       BZ /wait5

       ld /car_sp
       st /TXDATA

       HALT

val1    DATA H'F
car_H   DATA  h'48   ;-- "H"
car_O   DATA  h'4F   ;-- "O"
car_L   DATA  h'4C   ;-- "L"
car_A   DATA  h'41   ;-- "A"
car_sp  DATA  h'20   ;-- " "



          ORG 508
TXSTATUS  DATA    0  ;-- 508
TXDATA    DATA    0  ;-- 509
