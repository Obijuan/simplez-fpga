import unittest
from sasm3 import Lexer, Parser


def test_errors(asm):
    lexer = Lexer(asm)
    parser = Parser(lexer)
    try:
        prog = parser.parse()
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

asmfile6b = ("""
val1   DATA 10
val2   DATA h'FA
       DATA 1, 2, 3, 4, 5, 6
val3   DATA "a", 3, "b", "hola"
       DATA "sentence...."

     end
""")

asmfile7b = ("""
ini   LD /aa
hola  LD /20
      LD /H'100
      LD /val1

     end
""")

asmfile8b = ("""
ini   ST /h'100
      ST /aa
hola  ST /20
      ST /H'100
      ST /val1
      end
""")

asmfile9 = ("""
;-- Test 9
ini   ADD /h'100
      ADD /aa
hola  ADD /20
      ADD /H'100
      ADD /val1

     end
""")

asmfile10 = ("""
ini   BR /h'100
      BR /aa
hola  BR /20
      BR /H'100
      BR /val1

     end
""")

asmfile11 = ("""
ini   BZ /h'100
      BZ /aa
hola  BZ /20
      BZ /H'100
      BZ /val1

     end
""")

asmfile12 = ("""
ini   CLR
      DEC
      WAIT
fin   HALT

     end
""")

asmfile13 = ("""
;-- Test 13
    LD /val1
    ST /500
    ADD /100
    BR /ini
    BZ /loop

    CLR
    DEC
    WAIT
    HALT
     end
""")

asmfile14 = ("""
;-- Test 14

ini         EQU 10  ;-- Comienzo del programa
data_block  EQU 20  ;-- Dir bloque de datos

     org ini

     LD /val1
     ST /508

     HALT

     org data_block
     WAIT
     CLR

     end
""")

asmfile15 = ("""
;-- Data
val1 DATA h'0F, 1, 2, 3
     DATA 4

val2 DATA "hola"
     DATA "adios", "1", "2", "3"

     HALT
     end
""")

asmfile16 = ("""
val1 res 5
     res 10

     org 20
     res 1

     HALT
     end
""")

asmfile17 = ("""
ini   ld /val1
ini0  ld /val2
      HALT

;-- Data
val1 data 5
val2 data 10

     end
""")

asmfile18 = ("""
      BR /ini


      org 100

ini   ld /val1
      HALT

val1  DATA H'0f

     end
""")


class TestCase(unittest.TestCase):

    # -- Lexer tests
    def test_lexer_01(self):
        self.assertEqual(lexer_test(lex1), lex1_result)
"""
    # -- Errors
    def test_error_01(self):
        self.assertEqual(test_errors(ef1), "Error: END expected. Line: 2")

    def test_error_02(self):
        self.assertEqual(test_errors(ef2), "Error: No EOL after END. Line: 2")

    def test_error_03(self):
        self.assertEqual(test_errors(ef3), "Error: Label without instruction. Line: 3")

    def test_error_04(self):
        self.assertEqual(test_errors(ef4), "Error: Label without instruction. Line: 2")

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
# -- aQUI

    def test_09(self):
        self.assertEqual(test(asmfile9), True)

    def test_10(self):
        self.assertEqual(test(asmfile10), True)

    def test_11(self):
        self.assertEqual(test(asmfile11), True)

    def test_12(self):
        self.assertEqual(test(asmfile12), True)

    def test_13(self):
        self.assertEqual(test(asmfile13), True)

    def test_14(self):
        self.assertEqual(test(asmfile14), True)

    def test_15(self):
        self.assertEqual(test(asmfile15), True)

    def test_16(self):
        self.assertEqual(test(asmfile16), True)

    def test_17(self):
        self.assertEqual(test(asmfile17), True)

    def test_18(self):
        self.assertEqual(test(asmfile18), True)
"""

# -- Main program
if __name__ == '__main__':
    unittest.main()
