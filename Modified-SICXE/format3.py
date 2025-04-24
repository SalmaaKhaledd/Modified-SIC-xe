from formats import *
from symtab import *
from literals import *
from tables import *

class Format3(Format):
     
     def __init__(self, base, symtab,littab, source_line):
        self._base = base
        self._symtab = symtab
        self._littab=littab  
        self._location = source_line.loc
        self._mnemonic = source_line.mnemonic
        self._flags, self._n, self._i = determine_flags(source_line)
        self._disp = source_line.operand   #contains address of operand
        self._line_number = source_line.lineNum
        self._contents = source_line
     
     def generate(self):
         
         """ manipulating in int form and then converting to binary string then to hex for object code representation"""

         if self._mnemonic is None:
            raise LineFieldsError(message="A mnemonic was not specified.")
         
         output = ""
         opcode_lookup = int(str(op_table[self._mnemonic].opcode), 16) #converted to int for manipulation
         if self._n:
            opcode_lookup += 2
         if self._i:
            opcode_lookup += 1

         op = twos_complement(opcode_lookup, 6) # opcode converted to 6-bit binary string
         is_digit = False
         has_operands = False

         if self._disp is not None and not literal(self._contents.operand):
            has_operands = True
            if indexed(self._disp):
                self._disp = self._disp[:len(self._disp)-2]
                symbol_address,blockno = self._symtab.retrieve_label(self._disp)   #hex_value
            elif indirect(self._disp):
                self._disp = self._disp[1:]
                symbol_address,blockno = self._symtab.retrieve_label(self._disp)
            elif immediate(self._disp):
                self._disp = self._disp[1:]
                if str(self._disp).isdigit():
                    symbol_address = self._disp #decimal value
                    print("immediate address")
                    print(symbol_address)
                    is_digit = True  #no relative addressing
                else:
                    symbol_address,blockno = self._symtab.retrieve_label(self._disp)
            else:
                symbol_address,blockno = self._symtab.retrieve_label(self._contents.operand)
                #symbol_address = self._symtab.get(self._contents.operand)
            
            if symbol_address is not None:
                self._disp = symbol_address
            else:
                raise UndefinedSymbolError(message='Undefined symbol on line: ' +str(self._line_number+2), code=1,contents=self._contents)
            
         elif(self._disp is not None and literal(self._contents.operand)):
               has_operands = True 
               symbol_address,blockno = self._symtab.retrieve_label(self._contents.operand[1:])  #address of literal
               if symbol_address is not None:
                self._disp = symbol_address
               else:
                  self._disp = 0
                  raise UndefinedSymbolError(
                          message='Undefined literal on line: ' +
                          str(self._line_number+1), code=1,
                          contents=self._contents)
         else:                   #no operands
            has_operands = False 
            self._disp = 0
            raise LineFieldsError(message="Operand in none.Instruction 3 must have an operand.")
         
         #here self._disp contains the target address of the operand
         
         if  has_operands and not is_digit:
            # Try PC relative then base relative, or raise an error
            if (-2048 <= self.__pc_relative() <= 2047):
                self._flags += flag_table['p']
                disp = twos_complement(self.__pc_relative(), 12)  #can be -ve displacement -->binary representation of 2's complement 
               
            elif(0 <= self.__base_relative() <= 4095):
                self._flags += flag_table['b']
                disp = to_binary(self.__base_relative()).zfill(12)
                print("disp")
                print(disp)
            else:
                raise InstructionError(
                    message="Neither PC or Base relative addressing could be used.")
               
         else:  #is digit
            disp = twos_complement(int(self._disp), 12)
         flags = to_binary(hex(self._flags))
         output += op
         print("op")
         print(op)
         output += flags.zfill(4)
         print("flags")
         print(flags)
         output += disp
         print("output")
         print(output)
         objCode = hex(int(output, 2))[2:].zfill(6).upper()
         return objCode




     def __pc_relative(self):
        """ Calculate the PC relative address. """
        print("Target address in hex")
        print(self._disp)
        TA = int(str(self._disp), 16)   #target address
        print("Target address in decimal")
        print(TA)
        disp = TA- int(self._location)-3  #displacement
        print("disp")
        print(disp)
        return (disp)

     def __base_relative(self):
        """ Calculate the Base relative address. """
        if self._base is None:
            raise InstructionError(message="BASE directive not set")
        base = int(str(self._base), 16)
        disp = int(str(self._disp), 16)

        return (disp - base)


     def __len__(self):
        return 3

     def __repr__(self):
        return "<Format3: mnemonic=%s n=%s i=%s flags=%s disp=%s>" % \
                (self._mnemonic, self._n, self._i, self._flags, self._disp)

             
            
            
                        
                      
