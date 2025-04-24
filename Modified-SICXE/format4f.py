#yosra
from formats import *
from tables import *
"""
SYNTAX::  CADD T, LABEL, V 
-->CADD: opcode = 0BC --> opcode bits = 1011 11  
--> T: register --> regno=5 --> reg bits = 0101
--> LABEL: direct memory address fetched from symbol table 
--> V: overflow flag --> flag bits = 00

"""
class Format4f(Format):

    """
    format 4f instruction (conditional)

        6      4      2     20
    ------------------------------
    |opcode | reg | flag | address|
    -------------------------------
    """
    def __init__(self, mnemonic ,r, f , address):
        self.mnemonic = mnemonic
        self.r = r
        self.f = f
        self.address = address #hex

    def generate(self):

        output = "" 

        old_opcode = op_table[self.mnemonic].opcode
        new_opcode = to_binary(old_opcode)[:-2]
        new_opcode = new_opcode.zfill(6) 
        output += str(new_opcode)

        if self.r is not None:
            reg= registers_table[self.r]
            reg_hex = str(hex(reg))[2:]        #register might not be present--> CJUMP
        else: 
            reg_hex = "0"
        output += str(to_binary(reg_hex).zfill(4)) 

        flag = bin(flag_table2[self.f])[2:].zfill(2)
        output += flag

        address = to_binary(self.address).zfill(20)
        output += str(address)

        obj_code = hex(int(output, 2))[2:].upper()
        return obj_code


    def __len__(self):
        return 4

    def __repr__(self):
        return "<Format4f: mnemonic=%s r=%s address=%s flag=%s>" % (self.mnemonic, self.r, self.address, self.f)  