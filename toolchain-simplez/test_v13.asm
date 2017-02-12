;-------------------------------------------------------------------
; Prueba de referencia de direcciones. (e.j @inicio).
;-------------------------------------------------------------------
; Para pruebas ejecutar el compilador en formato parlanchín. :)
;    sasm -verbose test_v13.asm
;-------------------------------------------------------------------
;--
;-- Autor: Juan Manuel Rico (juanmard).
;-- Fecha: Febrero de 2017.
;-- Versión: 1.0.1
;-- 
;-------------------------------------------------------------------
inicio  WAIT
        WAIT
        LD  /inicio
        ADD /inicio
        ST  /inicio
prb     BR  /inicio
        LD  @prb
        ST  @prb
        ADD @prb
        BR  @prb
        HALT
datos   DATA prb
; datos_err  DATA @prb    ; En este caso da error.
                          ; Solo se admiten las referencias en instrucciones, no en directivas. 
END
