; Programa de ejemplo para Simplez
; EJEMPLO 1: Suma de dos numeros
; Version SIN ETIQUETAS, tal cual aparece en la pag 61 (Leccion 2, apartado 2.2) del libro
;   "Conceptos basicos de arquitectura y sistemas operativos. Curso de ordenadores" de
;   Gregorio Fernandez

;-- El programa comienza aqui

        ld /10
        add /11
        st /12
        HALT

        org 10
        DATA H'7
        DATA H'8
        DATA 0

end
