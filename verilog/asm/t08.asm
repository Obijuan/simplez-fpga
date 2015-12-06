;-- Programas de prueba para Simplez
;-- t08.asm: Pruebas de ADD: contador en los leds


       ld /val1   ; Inicializar acumulador
bucle  WAIT
       add /uno   ; Incrementar en uno
       BR /bucle   ; Repetir

;--- Datos
val1    DATA  h'1
uno     DATA  h'1
