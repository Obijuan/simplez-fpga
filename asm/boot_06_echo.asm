;-------------------------------------------------------------------------------------------
;-- Programa de ejemplo para Bootloader. Eco por pantalla de lo recibido por teclado
;--
;-- Este programa se carga mediante el bootloader
;--------------------------------------------------------------------------------------------


;-- Acceso a los perifericos
LEDS      EQU 507
TXSTATUS  EQU 508
TXDATA    EQU 509
RXSTATUS  EQU 510
RXDATA    EQU 511


        ORG h'40

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


end
