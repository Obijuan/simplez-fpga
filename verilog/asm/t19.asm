;-- Programas de prueba para Simplez
;-- t19.asm: Prueba de eco: todo lo que recibe SIMPLEZ por el teclado se envia
;-- a la pantalla


       ld /val1
       WAIT
loop
       ld /RXSTATUS    ;-- Esperar a que llegue un caracter
       BZ /loop

       ld /RXDATA     ;-- Leer el dato recibido
       st /car        ;-- Y almacenarlo

       ;-------- Hacer eco"
       ;-- Esperar a que este lista la pantalla
wait1
       ld /TXSTATUS    ;-- Leer el registro de estado de la pantalla
       BZ /wait1       ;-- Esperar a que se ponga a 1

       ;-- Enviar el caracter recibido
       ld /car
       st /TXDATA      ;-- Escribiendo en el registro de datos
       BR /loop
       HALT

val1   DATA H'FF
car    DATA 0


;-- Direcciones de acceso a pantalla y teclado

          ORG 508
TXSTATUS  DATA    0  ;-- 508:  Registro de estado
TXDATA    DATA    0  ;-- 509:  Registro de datos

;-- Direcciones de acceso al teclado
RXSTATUS  DATA    0  ;-- 510:  Registro de estado
RXDATA    DATA    0  ;-- 511:  Registro de datos
