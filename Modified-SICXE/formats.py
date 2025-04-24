from instruction import *
from errors import *
from tables import *

class Format(object):
    """ Base Instruction Format class. """

def determine_format(mnemonic):
        if extended(mnemonic):
            return op_table[mnemonic[1:]].format + 1
        else:
            return op_table[mnemonic].format

    
def to_binary(hex_string):
    return bin(int(str(hex_string), 16))[2:]

def twos_complement(value, length):
    if value < 0:
        value = (1 << length) + value
    out_format = '{:0%ib}' % length
    
    return out_format.format(value) #return binary string of value

def determine_flags(source_line):
        #Calculate the flags given a SourceLine object.
      
        flags = 0   #binary num initialized to 0 
        n = False
        i = False

        if immediate(source_line.operand):
              i = True
        elif indirect(source_line.operand):
              n = True
        else:
            n, i = True, True

        if indexed(source_line.operand):
            if (not n and not i) or (n and i):  #to allow sic-compatible mode (n&i=0 , indexed addr. allowed)
                  flags += flag_table['x']
            else:
                  raise LineFieldsError(message="Indexed addressing cannot be combined with immediate or indirect modes.")
        if extended(source_line.mnemonic):
            flags += flag_table['e']
        return flags, n, i