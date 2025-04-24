from errors import LineFieldsError
from instruction import *
from tables import *
from formats import *

class Format2(Format):
    """ Format 2 instruction class.

         8       4     4
     ======================
    |    op    | r1 |  r2  |
     ======================

    """
    def __init__(self, mnemonic, r1, r2):
        self._mnemonic = mnemonic
        self._r1 = r1
        self._r2 = r2

    def generate(self):
        """ Generate the machine code for the instruction. """
        if self._mnemonic is None:
            raise LineFieldsError(message="A mnemonic was not specified.")

        output = ""

        # lookup the opcode
        opcode_lookup = op_table[self._mnemonic].opcode
        output += str(opcode_lookup)

        # look up the registers
        r1_lookup = registers_table[self._r1]
        stripped_r1 = str(hex(r1_lookup)).lstrip("0x") or "0"
        output += str(stripped_r1)

        if self._r2 is not None:
            r2_lookup = registers_table [self._r2]
            stripped_r2 = str(hex(r2_lookup)).lstrip("0x") or "0"
            output += str(stripped_r2)
        else:
            output += "0"

        return output

    def __len__(self):
        return 2

    def __repr__(self):
        return "<Format2: mnemonic=%s r1=%s r2=%s>" % (self._mnemonic, self._r1, self._r2)
