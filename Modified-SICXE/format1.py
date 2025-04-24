from errors import LineFieldsError
from instruction import *
from tables import *
from formats import *

class Format1(Format):
    """ Format 1 instruction class.

         8
     ==========
    |    op    |
     ==========

    """
    def __init__(self, mnemonic):
        self._mnemonic = mnemonic

    def generate(self):
        """ Generate the machine code for the instruction. """
        if self._mnemonic is None:
            raise LineFieldsError(message="A mnemonic was not specified.")

        output = ""
        # lookup the opcode
        opcode_lookup = op_table[self._mnemonic].opcode
        output += str(opcode_lookup)

        return output

    def __len__(self):
        return 1

    def __repr__(self):
        return "<Format1: mnemonic=%s>" % self._mnemonic

