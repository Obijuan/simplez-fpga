
    ;-- Test 1

ini         EQU 10  ;-- Comienzo del programa
data_block  EQU 20  ;-- Dir bloque de datos

     org ini

     LD /100
     ST /508

     HALT

     org data_block
     WAIT
     CLR

     end
