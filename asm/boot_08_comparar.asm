;-------------------------------------------------------------------------------------------
;-- Programa de ejemplo para Bootloader.
;-- Deberá cargarse el programa una vez compilado en modo interativo desde consola:
;--       # sboot -i prog.list
;-------------------------------------------------------------------------------------------
;-- Programa que compara los datos de dos registros y realiza tres retornos distintos
;--   según el resultado de la comparación:
;--
;--     * dato1 > dato2 (ret_mayor).
;--     * dato1 = dato2 (ret_iguales).
;--     * dato1 < dato2 (ret_menor).
;--
;--   donde 'dato1' y 'dato2' son los registros que contienen los valores a comparar.
;--
;-- Simplez-F, al no disponer de pila para las llamadas a función. Debe realizar una
;--   adaptación previa de los parámetros y de las direcciones de retorno, modificando
;--   directamente el código de la memoria mediante el uso de un salto incondicional (BR). 
;-------------------------------------------------------------------------------------------
;--
;-- Autor: Juan Manuel Rico (juanmard).
;-- Fecha: Febrero de 2017.
;-- Versión: 1.0
;-- 
;--------------------------------------------------------------------------------------------

;-- Acceso a los perifericos
LEDS      EQU 507
TXSTATUS  EQU 508
TXDATA    EQU 509
RXSTATUS  EQU 510
RXDATA    EQU 511


ORG h'40
; Lee primer dato como caracter ASCII del puerto serie.
leer_1    LD  /RXSTATUS
          BZ  /leer_1
          LD  /RXDATA
          ST  /dato1

; Se muestra por pantalla.
write_1   LD  /TXSTATUS
          BZ  /write_1
          LD  /dato1
          ST  /TXDATA

; Lee segundo dato como caracter ASCII del puerto serie.
leer_2    LD  /RXSTATUS
          BZ  /leer_2
          LD  /RXDATA
          ST  /dato2

; Se muestra por pantalla.
write_2   LD  /TXSTATUS
          BZ  /write_2
          LD  /dato2
          ST  /TXDATA

main      LD  /br_code          ; Se preparan direcciones de destino.
          ADD /direc_menor
          ST  /ret_menor
          LD  /br_code
          ADD /direc_iguales
          ST  /ret_iguales
          LD  /br_code
          ADD /direc_mayor
          ST  /ret_mayor
          BR  /comparar

          ; Ejecuta si menor.
          LD  /salida1
          ST  /LEDS
          BR  /fin

          ;Ejecuta si iguales.
          LD  /salida2
          ST  /LEDS
          BR  /fin

          ; Ejecuta si mayor.
          LD  /salida3
          ST  /LEDS
          BR  /fin

; Se vuelve al inicio tras una pausa de 400ms.
fin       WAIT
          WAIT
          CLR
          BR  /leer_1

;----------------------------;
;--       Subrutinas       --;
;----------------------------;

;------------------------------------------------------
; Compara dos datos que se cargaron en memoria.
;------------------------------------------------------
; El algoritmo consiste en ir restando ambos datos y
;  ver cual de ellos se hace antes cero.
;------------------------------------------------------
comparar       LD   /dato1
               DEC
               BZ   /cero_dato1
               ST   /dato1
               LD   /dato2
               DEC
               BZ   /cero_dato2
               ST   /dato2
               BR   /comparar

; El dato1 llego antes a cero que dato 2.
cero_dato1     ST   /dato1
               LD   /dato2
               DEC
               BZ   /ret_iguales
               ST   /dato2
ret_menor      DATA 0               ; dato1 < dato2
ret_iguales    DATA 0               ; dato1 = dato2

; El dato2 llego antes a cero que dato 1.
cero_dato2     ST   /dato2
ret_mayor      DATA 0

;----------------------------;
;-- Variables y constantes --;
;----------------------------;
br_code        BR    /0
dato1          DATA  0
dato2          DATA  0
direc_menor    DATA  H'5A
direc_iguales  DATA  H'5D
direc_mayor    DATA  H'60
salida1        DATA  H'01
salida2        DATA  H'02
salida3        DATA  H'04

end
