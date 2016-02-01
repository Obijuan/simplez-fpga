import unittest
from sasm import Lexer, Parser


def test_errors(asm):
    lexer = Lexer(asm)
    parser = Parser(lexer)

    # -- Syntax analysis
    try:
        prog = parser.parse()
    except Exception as inst:
        msg, = inst.args
        return msg

    # -- Semantic analysis
    try:
        prog.solve_labels()
    except Exception as inst:
        msg, = inst.args
        return msg

# -- Error: No end directive
ef1 = (
 """
 """)

# -- Error: After the end directive there should be an EOL
ef2 = ("""
end 2
""")

# -- Error: Label without instruction
ef3 = ("""

   hello

""")

# -- Error: Label without instruction (they should be in the same line)
ef4 = ("""
hello
       HALT

end
""")

# -- Error: No end directive
ef5 = ("""
hello HALT

""")

# -- Error. ORG without number or label
ef6 = ("""
    org

end
""")

# -- Error. Unknow label
ef7 = ("""
  org hello

end
""")

# -- Error. EQU directive without label
ef8 = ("""
   EQU

""")

# -- Error. Invalid label
ef9 = ("""
h'23 EQU 10
""")

# -- Error. Invalida data
ef10 = ("""
hello   EQU  EQU
""")

# -- Error. Invalid element
ef11 = ("""
stop  HALT  adf   ;-- finish

end
""")

ef12 = ("""
;-- 2 words program
;-- With verbosity
ini EQU 0

      org ini  ;-- Initial

      WAIT ;-- hola
      WAIT 2 ;<-- There is a sintax error here
end2  HALT  ;-- Stop

end
""")

ef13 = ("""
bra ini  ;-- Syntax error

WAIT
halt

end
""")

ef14 = ("""

     br ini  ; <-- Error. Label not defined

     end
""")

ef15 = ("""
     br ini  ; <-- Error. It should be br /ini

ini  HALT
     end
""")

ef16 = ("""
     br /ini  ; <= Error: Symbol not defined

     HALT
     end
""")

ef17 = ("""
ini  EQU 1

     br /ini

ini  HALT  ; <= Error. Duplicated label

     end
""")

ef18 = ("""
     WAIT
     HALT

x1    DATA VAL1

     end
""")

ef19 = ("""
VAL1 EQU 1

     WAIT
     HALT

x1    DATA h'VAL1

     end
""")


# -- Lexer tests
def lexer_test(asmfile):
    lexer = Lexer(asmfile)
    log = lexer.test()
    return log

# -- All the possible tokens
lex1 = ("""
  ;Comment
  label 102 h'FA /504 /h'100  "string" ,
ORG EQU RES DATA END
ST LD ADD BR BZ CLR DEC WAIT HALT
[""")

lex1_result = ("""[1] Token: EOL
[2] Token: COMMENT (Comment)
[2] Token: EOL
[3] Token: LABEL (label)
[3] Token: NUMBER (102)
[3] Token: NUMBER (250)
[3] Token: ADDR (504)
[3] Token: ADDR (256)
[3] Token: STRING (string)
[3] Token: COMMA
[3] Token: EOL
[4] Token: ORG
[4] Token: EQU
[4] Token: RES
[4] Token: DATA
[4] Token: END
[4] Token: EOL
[5] Token: ST
[5] Token: LD
[5] Token: ADD
[5] Token: BR
[5] Token: BZ
[5] Token: CLR
[5] Token: DEC
[5] Token: WAIT
[5] Token: HALT
[5] Token: EOL
[6] Token: Unknown ([)
[6] Token: EOF
""")


def test(asmfile):
    lexer = Lexer(asmfile)
    parser = Parser(lexer)
    prog = parser.parse()
    prog.solve_labels()
    mcode = prog.machine_code()
    return mcode


# -- Blank program. It compiles ok, but the output machine code is blank
asmfile1 = ("""
;-- Test 1
end
""")

# -- Testing EOL. Same program than before
asmfile2 = ("""



end
""")

# -- Another ok Blank program
asmfile3 = ("""
;-- Comment 1
  ;-- Comment 2


  end
""")

# -- Blank program
asmfile4 = ("""
begin   EQU  20

      org begin

end
""")

# -- Blank program. EQU test
asmfile5 = ("""
a    equ 0
b    equ 1
c    equ 2
d    equ 3
e    equ 4
f    equ 5
g    equ 6
h    equ 7
i    equ 8
j    equ 9
k    equ 10
end
""")

# -- blank program. ORG test
asmfile6 = ("""
;-- Comentario 1
;-- Comentario 2

block EQU 30

     org 0

     org 100

     org H'100

     org 512     ;-- Comentario 3

     org block

     end
""")

# -- 1 word program
asmfile7 = ("""
HALT
end
""")

# -- Same 1 word program, but more verbose
asmfile8 = ("""
;-- 1 word program
;-- It does nothing: just stops

ini   EQU  0

      org ini  ;-- Initial memory

stop  HALT     ;-- finish

end
""")

# -- 2 words program
asmfile9 = ("""
WAIT
HALT
end
""")

asmfile10 = ("""
;-- 2 words program
;-- With verbosity
ini EQU 0

      org ini  ;-- Initial

      WAIT  ;-- Wait 200ns
end2  HALT  ;-- Stop

end
""")

asmfile11 = ("""
;-- Wait test
;-- Wait for 1 sec before ending
ini EQU 0

      org ini  ;-- Initial

      WAIT ;-- hola
etiq  WAIT
etiq2 WAIT  ;-- Useless
      WAIT
WAIT

end2  HALT  ;-- Stop

end
""")

# -- DATA test
asmfile12 = ("""
val1   DATA 0
       data H'E00   ;-- Halt in machine code ;-)
       DaTa 1     ;No label
       DatA 2
val2   DATA h'FA
val4   data h'001, H'CAF
       DATA 1, 2, 3, 4, 5, 6
val3   DATA "a", 3, "b", "hola"  ;- Ascii
       DATA "sentence...."
     end
""")

asmfile12_mcode = ("""000\nE00\n001\n002\n0FA\n001\nCAF\n001\n002\n003
004\n005\n006\n061\n003\n062\n068\n06F\n06C\n061\n073\n065\n06E\n074
065\n06E\n063\n065\n02E\n02E\n02E\n02E
""")

asmfile13 = ("""
     br /ini

ini  HALT

     end
""")

asmfile14 = ("""
ini EQU 1

     br /ini

     HALT

     end
""")

asmfile15 = ("""
ini   LD /aa
hola  LD /20
      LD /H'100
      LD /val1
      HALT

aa    DATA h'0F
val1  DATA 10
      end
""")

asmfile16 = ("""
      CLR
ini   ST /h'100
      ST /aa
hola  ST /20
      ST /H'100
      ST /val1
      HALT

aa    RES 1
val1  DATA 0

      end
""")

asmfile17 = ("""
;-- Test ADD
ini   ADD /h'100
      ADD /aa
hola  ADD /20
      ADD /H'100
      ADD /val1
      HALT

aa    RES 2
val1  DATA "a"

     end
""")

asmfile18 = ("""
aa     EQU h'200

ini0   BR /h'100
       BR /aa
hola1  BR /20
       BR /H'100
       BR /val1

val1   HALT

     end
""")

asmfile19 = ("""
      CLR
      BZ /ini

ini   BZ /h'100
      BZ /aa
hola  BZ /20
      BZ /H'100
      BZ /val1

val1 EQU 20

      org 100
aa    HALT

     end
""")

asmfile20 = ("""
ini   CLR
      DEC
      WAIT
fin   HALT

     end
""")

asmfile21 = ("""
;-- Test 21

loop    LD /val1
        ST /500
        ADD /100
        BZ /loop
        BR /stop

         CLR
         DEC
         WAIT
stop     HALT
val1 DATA h'AA
     end
""")

asmfile22 = ("""
 ;-- Test 22

 ini         EQU 10  ;-- Comienzo del programa
 data_block  EQU 20  ;-- Dir bloque de datos

      org ini

      LD /val1
      ST /508

      HALT

      org data_block
      WAIT
      CLR
val1  DATA "a"

      end
""")


asmfile23 = ("""
val1 res 5
     res 10

     org 20
     res 1

     HALT
     end
""")

asmfile23_result = ("""000\n000\n000\n000\n000
000\n000\n000\n000\n000\n000\n000\n000\n000\n000\n@014\n000\nE00\n""")

asmfile24 = ("""
ini   ld /val1
ini0  ld /val2
      HALT

;-- Data
val1 data 5
val2 data 10

     end
""")

asmfile25 = ("""
      BR /ini


      org 100

ini   ld /val1
      HALT

val1  DATA H'0f

     end
""")

asmfile26 = ("""
VAL1 EQU 1
VAL2 EQU 2
VAL3 EQU 3

     WAIT
     HALT

x1    DATA VAL1
y     DATA VAL2, VAL3, 4, "5", h'6

     end
""")

# ---------------- Working examples

we01 = ("""
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
""")

we02 = ("""
;-- Programas de ejemplo para Simplez
;-- sec.asm: Sacar una secuencia de 2 estados por los leds

loop    LD /val1   ;-- Sacar valor 1 por los leds
        ST /LEDS
        WAIT       ; Pausa
        LD /val2   ;-- Sacar valor 2 por los leds
        ST /LEDS
        WAIT
        BR /loop   ;-- Repetir


;-- Datos
val1  DATA H'03   ;-- Valor 1 de la secuencia
val2  DATA H'0C   ;-- Valor 2 de la secuencia


;------ PERIFERICO: puerto de leds ------------------

          ORG 507

LEDS      DATA    0  ;-- Todo lo escrito aqui se saca por los leds

end
""")

we03 = ("""
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
""")

we03_result = ("""20F\n1FB\nF00\nA00\n1FB\n3FE\n805\n3FF\n1FB\n010
3FC\n80A\n210\n1FD\n605\n00F\n000\n@1FB\n000\n000\n000\n000\n000
""")


class TestCase(unittest.TestCase):

    # -- Lexer tests
    def test_lexer_01(self):
        self.assertEqual(lexer_test(lex1), lex1_result)

    # -- Errors
    def test_error_01(self):
        self.assertEqual(test_errors(ef1), "Error: END expected. Line: 2")

    def test_error_02(self):
        self.assertEqual(test_errors(ef2), "Error: No EOL after END. Line: 2")

    def test_error_03(self):
        self.assertEqual(test_errors(ef3), "Error: Invalid instruction. Line: 3")

    def test_error_04(self):
        self.assertEqual(test_errors(ef4), "Error: Invalid instruction. Line: 2")

    def test_error_05(self):
        self.assertEqual(test_errors(ef5), "Error: END expected. Line: 4")

    def test_error_06(self):
        self.assertEqual(test_errors(ef6), "Error: ORG: Label or number expected. Line: 2")

    def test_error_07(self):
        self.assertEqual(test_errors(ef7), "Error: Unknow Label: hello. Line: 2")

    def test_error_08(self):
        self.assertEqual(test_errors(ef8), "Error: EQU without label. Line: 2")

    def test_error_09(self):
        self.assertEqual(test_errors(ef9), "Error: Unexpected element. Line: 2")

    def test_error_10(self):
        self.assertEqual(test_errors(ef10), "Error: EQU: Expected a number. Line: 2")

    def test_error_11(self):
        self.assertEqual(test_errors(ef11), "Error: Unexpected element. Line: 2")

    def test_error_12(self):
        self.assertEqual(test_errors(ef12), "Error: Unexpected element. Line: 9")

    def test_error_13(self):
        self.assertEqual(test_errors(ef13), "Error: Invalid instruction. Line: 2")

    def test_error_14(self):
        self.assertEqual(test_errors(ef14), "Error: Invalid address. Line: 3")

    def test_error_15(self):
        self.assertEqual(test_errors(ef15), "Error: Invalid address. Line: 2")

    def test_error_16(self):
        self.assertEqual(test_errors(ef16), "Error: Line: 2: Symbol not defined: ini")

    def test_error_17(self):
        self.assertEqual(test_errors(ef17), "Error: Duplicated label: ini. Line: 6")

    def test_error_18(self):
        self.assertEqual(test_errors(ef18), "Error: Line: 5: Symbol not defined: VAL1")

    def test_error_19(self):
        self.assertEqual(test_errors(ef19), "Error: Unexpected element. Line: 7")

    # ------------ Code ok
    def test_01(self):
        self.assertEqual(test(asmfile1), "")

    def test_02(self):
        self.assertEqual(test(asmfile2), "")

    def test_03(self):
        self.assertEqual(test(asmfile3), "")

    def test_04(self):
        self.assertEqual(test(asmfile4), "")

    def test_05(self):
        self.assertEqual(test(asmfile5), "")

    def test_06(self):
        self.assertEqual(test(asmfile6), "")

    def test_07(self):
        self.assertEqual(test(asmfile7), "E00\n")

    def test_08(self):
        self.assertEqual(test(asmfile8), "E00\n")

    def test_09(self):
        self.assertEqual(test(asmfile9), "F00\nE00\n")

    def test_10(self):
        self.assertEqual(test(asmfile10), "F00\nE00\n")

    def test_11(self):
        self.assertEqual(test(asmfile11), "F00\nF00\nF00\nF00\nF00\nE00\n")

    def test_12(self):
        self.assertEqual(test(asmfile12), asmfile12_mcode)

    def test_13(self):
        self.assertEqual(test(asmfile13), "601\nE00\n")

    def test_14(self):
        self.assertEqual(test(asmfile14), "601\nE00\n")

    def test_15(self):
        self.assertEqual(test(asmfile15), "205\n214\n300\n206\nE00\n00F\n00A\n")

    def test_16(self):
        self.assertEqual(test(asmfile16), "A00\n100\n007\n014\n100\n008\nE00\n000\n000\n")

    def test_17(self):
        self.assertEqual(test(asmfile17), "500\n406\n414\n500\n408\nE00\n000\n000\n061\n")

    def test_18(self):
        self.assertEqual(test(asmfile18), "700\n800\n614\n700\n605\nE00\n")

    def test_19(self):
        self.assertEqual(test(asmfile19), "A00\n802\n900\n864\n814\n900\n814\n@064\nE00\n")

    def test_20(self):
        self.assertEqual(test(asmfile20), "A00\nC00\nF00\nE00\n")

    def test_21(self):
        self.assertEqual(test(asmfile21), "209\n1F4\n464\n800\n608\nA00\nC00\nF00\nE00\n0AA\n")

    def test_22(self):
        self.assertEqual(test(asmfile22), "@00A\n216\n1FC\nE00\n@014\nF00\nA00\n061\n")

    def test_23(self):
        self.assertEqual(test(asmfile23), asmfile23_result)

    def test_24(self):
        self.assertEqual(test(asmfile24), "203\n204\nE00\n005\n00A\n")

    def test_25(self):
        self.assertEqual(test(asmfile25), "664\n@064\n266\nE00\n00F\n")

    def test_26(self):
        self.assertEqual(test(asmfile26), "F00\nE00\n001\n002\n003\n004\n035\n006\n")

    # -- Working examples
    def test_we_01(self):
        self.assertEqual(test(we01), "203\n1FB\nE00\n00F\n@1FB\n000\n")

    def test_we_02(self):
        self.assertEqual(test(we02), "207\n1FB\nF00\n208\n1FB\nF00\n600\n003\n00C\n@1FB\n000\n")

    def test_we_03(self):
        self.assertEqual(test(we03), we03_result)

# -- Main program
if __name__ == '__main__':
    unittest.main()
