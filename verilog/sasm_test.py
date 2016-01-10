import unittest
from sasm3 import Lexer, Parser


def test(asmfile):
    print(asmfile)
    lexer = Lexer(asmfile)
    parser = Parser(lexer)
    parser.parse()
    return True


asmfile1 = ("""
;-- Test 1
end
""")

asmfile2 = ("""



end
""")

asmfile3 = ("""
;-- Comment 1
  ;-- Comment 2


  end
""")

asmfile4 = ("""
;-- Comentario 1
;-- Comentario 2

     org 0

     org 100

     org H'100

     org 512     ;-- Comentario 3

     end
""")

asmfile5 = ("""
    org hola


    org 0

    org H'00

    org H'CACA

    org inicio

     end
""")

asmfile6 = ("""
val1   DATA 10
val2   DATA h'FA
       DATA 1, 2, 3, 4, 5, 6
val3   DATA "a", 3, "b", "hola"
       DATA "sentence...."

     end
""")

asmfile7 = ("""
ini   LD /aa
hola  LD /20
      LD /H'100
      LD /val1

     end
""")

asmfile8 = ("""
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


class TestCase(unittest.TestCase):

    def test_01(self):
        self.assertEqual(test(asmfile1), True)

    def test_02(self):
        self.assertEqual(test(asmfile2), True)

    def test_03(self):
        self.assertEqual(test(asmfile3), True)

    def test_04(self):
        self.assertEqual(test(asmfile4), True)

    def test_05(self):
        self.assertEqual(test(asmfile5), True)

    def test_06(self):
        self.assertEqual(test(asmfile6), True)

    def test_07(self):
        self.assertEqual(test(asmfile7), True)

    def test_08(self):
        self.assertEqual(test(asmfile8), True)

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


# -- Main program
if __name__ == '__main__':
    unittest.main()
