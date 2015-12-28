;-- Programas de prueba para Simplez
;-- t21.asm: Prueba de perifericos
;-- Cada vez que se recibe un caracter por el puerto serie, se incrementa un contador
;-- que se visualiza por los leds

;-- Lanzar una rafaga por los leds, para indicar que arranca el programa
        LD /cval1
        ST /LEDS
        WAIT
        CLR
        ST /LEDS

;-- Inicializar contador
    CLRA
    ST /cont

;-- Bucle principal: Incrementar contador cada vez que se recibe un caracter
main

       ;-- Esperar a que llegue un caracter
       LD /RXSTATUS
       BZ /main

       ;-- Leer caracter
       LD /RXDATA

       ;-- Incrementar contador
       LD /cont
       ADD /uno
       ST /cont

       ;-- Sacar contador por los leds
       ST /LEDS

       BR /main

;-- Variables y constantes
cval1  DATA  H'0F   ;-- Valor constante
uno    DATA  H'01   ;-- Valor constante
cont   DATA  0      ;-- Contador

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
