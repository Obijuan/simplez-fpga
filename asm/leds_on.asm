;-- Programas de ejemplo para Simplez
;-- leds_on.asm: Encender todos los leds

    LD /val    ; Cargar en A valor a enviar al puerto de los leds
    ST /LEDS   ; Escribir valor en el puerto de leds
    HALT       ; Terminar

;-- Datos
val  DATA H'0F   ;-- Valor a sacar por los leds


;------ PERIFERICO: puerto de leds ------------------

          ORG 507

LEDS      DATA    0  ;-- Todo lo escrito aqui se saca por los leds

end
