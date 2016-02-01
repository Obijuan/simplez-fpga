;-- Programas de ejemplo para Simplez
;-- eco.asm: Se hace eco de lo recibido por el puerto serie y ademas se saca por los leds

;-- Lanzar una rafaga por los leds, para indicar que arranca el programa
        LD /cval1
        ST /LEDS
        WAIT
        CLR
        ST /LEDS

;-- Bucle principal: Incrementar contador cada vez que se recibe un caracter

main   LD /RXSTATUS  ;-- Esperar a que llegue un caracter
       BZ /main

       ;-- Leer caracter
       LD /RXDATA

       ;-- Sacarlo por los leds
       ST /LEDS

       ;-- Alcacenar caracter recibido
       ST /car

       ;-- Enviarlo de vuelta

txloop  LD /TXSTATUS  ;-- Esperar a que pantalla lista
        BZ /txloop

       ;-- Sacarlo por pantalla
       LD /car
       ST /TXDATA

       BR /main

;-- Variables y constantes
cval1  DATA  H'0F   ;-- Valor constante
car    DATA  0      ;-- Caracter recibido


;------ PERIFERICOS ------------------

          ORG 507
;-- LEDS
LEDS      DATA    0  ;-- 507: Escritura en leds


;--- PANTALLA
TXSTATUS  DATA    0  ;-- 508:  Registro de estado
TXDATA    DATA    0  ;-- 509:  Registro de datos

;-- Direcciones de acceso al teclado
RXSTATUS  DATA    0  ;-- 510:  Registro de estado
RXDATA    DATA    0  ;-- 511:  Registro de datos

end
