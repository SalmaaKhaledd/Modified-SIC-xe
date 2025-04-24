
from instruction import Instr

op_table = { 'ADD':     Instr('18', 3, ['m']), 
             'ADDF':    Instr('58', 3, ['m']),
             'ADDR':    Instr('90', 2, ['r1', 'r2']),
             'AND':     Instr('40', 3, ['m']),
             'CLEAR':   Instr('B4', 2, ['r1']),
             'COMP':    Instr('28', 3, ['m']),
             'COMPF':   Instr('88', 3, ['m']),
             'COMPR':   Instr('A0', 2, ['r1', 'r2']),
             'DIV':     Instr('24', 3, ['m']),
             'DIVF':    Instr('64', 3, ['m']),
             'DIVR':    Instr('9C', 2, ['r1', 'r2']),
             'FIX':     Instr('C4', 1, None),
             'FLOAT':   Instr('C0', 1, None),
             'HIO':     Instr('F4', 1, None),
             'J':       Instr('3C', 3, ['m']),
             'LDA':     Instr('00', 3, ['m']),
             'LDB':     Instr('68', 3, ['m']),
             'LDCH':    Instr('50', 3, ['m']),
             'LDF':     Instr('70', 3, ['m']),
             'LDL':     Instr('08', 3, ['m']),
             'LDS':     Instr('6C', 3, ['m']),
             'LDT':     Instr('74', 3, ['m']),
             'LDX':     Instr('04', 3, ['m']),
             'LPS':     Instr('D0', 3, ['m']),
             'MUL':     Instr('20', 3, ['m']),
             'MULF':    Instr('60', 3, ['m']),
             'MULR':    Instr('98', 2, ['r1', 'r2']),
             'NORM':    Instr('C8', 1, None),
             'OR':      Instr('44', 3, ['m']),
             'RD':      Instr('D8', 3, ['m']),
             'RMO':     Instr('AC', 2, ['r1', 'r2']),
             'RSUB':    Instr('4C', 3, None),
             'SHIFTL':  Instr('A4', 2, ['r1', 'n']),
             'SHIFTR':  Instr('A8', 2, ['r1', 'n']),
             'SIO':     Instr('F0', 1, None),
             'SSK':     Instr('EC', 3, ['m']),
             'STA':     Instr('0C', 3, ['m']),
             'STB':     Instr('78', 3, ['m']),
             'STCH':    Instr('54', 3, ['m']),
             'STF':     Instr('80', 3, ['m']),
             'STI':     Instr('D4', 3, ['m']),
             'STL':     Instr('14', 3, ['m']),
             'STS':     Instr('7C', 3, ['m']),
             'STSW':    Instr('E8', 3, ['m']),
             'STT':     Instr('84', 3, ['m']),
             'STX':     Instr('10', 3, ['m']),
             'SUB':     Instr('1C', 3, ['m']),
             'SUBF':    Instr('5C', 3, ['m']),
             'SUBR':    Instr('94', 2, ['r1', 'r2']),
             'SVC':     Instr('B0', 2, ['m']),
             'TD':      Instr('E0', 3, ['m']),
             'TIO':     Instr('F8', 1, None),
             'TIX':     Instr('2C', 3, ['m']),
             'TIXR':    Instr('B8', 2, ['r1']),
             'WD':      Instr('DC', 3, ['m']),
             
             'CADD':    Instr('BC', 4, ['r','m','f']),
             'CSUB':    Instr('8C', 4, ['r','m','f']),
             'CLOAD':   Instr('E4', 4, ['r','m','f']),
             'CSTORE':  Instr('FC', 4, ['r','m','f']),
             'CJUMP':   Instr('CC', 4, ['m','f']), 
             }

#format 3 and 4
flag_table = { 'n': 0b100000,
               'i': 0b010000,
               'x': 0b001000,
               'b': 0b000100,
               'p': 0b000010,
               'e': 0b000001
             }

#format 4f
flag_table2 = { 'Z' : 0b00,
                'N': 0b01,
                'C': 0b10,
                'V':0b11 }

registers_table = {'A':  0,
                   'X':  1,
                   'L':  2,
                   'B':  3,
                   'S':  4,
                   'T':  5,
                   'F':  6,
                   'PC': 8,
                   "SW": 9
                  }

block_table={ "DEFAULT" : 0,
              "DEFAULTB" : 1,
               "CDATA": 2,
               "CBLKS": 3
}

""" after HIO
             'J':       Instr('3C', 3, ['m']),
             'JEQ':     Instr('30', 3, ['m']),
             'JGT':     Instr('34', 3, ['m']),
             'JLT':     Instr('38', 3, ['m']),
             'JSUB':    Instr('48', 3, ['m']),
             """