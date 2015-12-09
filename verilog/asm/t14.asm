;-- Programas de prueba para Simplez
;-- t14.asm: Prueba de escritura en la pantalla. Registro de datos


       ld /car1
       st /TXDATA   ;-- Escribir en pantalla
       WAIT         ;-- No se usa el registro de status. Se espera un tiempo

       ld /car2
       st /TXDATA
       HALT

;--- Datos
car1  DATA  h'48   ;-- "H"
car2  DATA  h'4F   ;-- "O"

        ORG 509
TXDATA  DATA 0
