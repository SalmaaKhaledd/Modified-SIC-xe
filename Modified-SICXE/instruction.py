

class Instr(object):
    
    """ Represents a single instruction.
        only utilized in building optable
    """
    def __init__(self, opcode, format, operands):
        self.__opcode = opcode
        self.__format = format
        self.__operands = operands

    @property
    def opcode(self):
        return self.__opcode

    @property
    def format(self):
        return self.__format

    @property
    def operands(self):
        return self.__operands
    
 
# Indexed addressing
indexed = lambda x: str(x).endswith(',X')
# Indirect addressing
indirect = lambda x: str(x).startswith('@')
# An immediate operand
immediate = lambda x: str(x).startswith('#')
# An extended format instruction
extended = lambda x: str(x).startswith('+')
# Literal
literal = lambda x: str(x).startswith('=')  
# Block
block = lambda x: str(x).startswith('USE')
hex_value= lambda x: str(x).startswith("X'") 
ascii_value= lambda x: str(x).startswith("C'") 