from formats import *
from tables import *
from errors import*
from symtab import*


class Format4(Format):
    """ Format 4 instruction class.

        6      1   1   1   1   1   1              20
     ============================================================
    |   op   | n | i | x | b | p | e |          address          |
     ============================================================
    """
   
    def __init__(self, symtab,littab, source_line):
        self._symtab=symtab
        self._littab=littab                 
        self._location=source_line.loc  
        self._mnemonic = source_line.mnemonic 
        self._flags, self._n, self._i = determine_flags(source_line)
        self._disp = source_line.operand      
        self._line_number = source_line.lineNum   
        self._contents = source_line        
      
    def generate(self):
     
        if self._mnemonic is None:
            raise LineFieldsError(message="A mnemonic was not specified.")
        

        output = ""
        opcode_lookup = int(str(op_table[self._mnemonic[1:]].opcode), 16) #opcode converted to int for manipulation
        if self._n:
            opcode_lookup += 2 # Set the n-bit
        if self._i:
            opcode_lookup += 1 # Set the i-bit
        op = twos_complement(opcode_lookup, 6) # opcode converted to 6-bit binary string

        #resolve operand into an absolute address

        if self._disp is not None and not literal(self._disp): #has operand & not literal
            if indexed(self._disp): #handles indexed addressing
                self._disp = self._disp[:len(self._disp)-2]
                symbol_address,blockno = self._symtab.retrieve_label(self._disp) #If symbolic (label), look up in symtab
                #symbol_address = self._symtab.get(self._disp) 

            elif immediate(self._disp):
                self._disp = self._disp[1:] 	# Strip # and check if the operand is a numeric value.
                if str(self._disp).isdigit():  #If numeric, convert to hex
                    symbol_address = hex(int(self._disp))[2:] 
                else:
                    symbol_address,blockno = self._symtab.retrieve_label(self._disp) #If symbolic (label), look up in symtab
                    print('label address')
                    print(symbol_address)
            elif indirect(self._disp):                 #handles indirect addressing
                  self._disp = self._disp[1:]
                  if str(self._disp).isdigit():
                    symbol_address = hex(int(self._disp))[2:] #If numeric, convert to hex
                  else:
                    symbol_address,blockno = self._symtab.retrieve_label(self._disp) #If symbolic (label), look up in symtab
                    print('label address')
                    print(symbol_address)

            else: #simple addressing
                print('simple addressing')
                print(self._disp)
                print(self._contents.operand)
                symbol_address,blockno = self._symtab.retrieve_label(self._disp) #test
                print('label address')
                print(symbol_address)
            if symbol_address is not None:
                self._disp = symbol_address
            else:
                self._disp = 0
                raise UndefinedSymbolError(
                        message='Undefined symbol on line: ' +
                        str(self._line_number+1), code=1,
                        contents=self._contents)
        
            

        elif(self._disp is not None and literal(self._disp)):  #has operand & literal
            self._disp=self._littab.retrieve_lit(self._disp[1:]) #test 
            symbol_address=self._disp[2]  #address of literal
            print('literal address')
            print(self._disp)

            if symbol_address is not None:
                self._disp = symbol_address
            else:
                self._disp = 0
                raise UndefinedSymbolError(
                        message='Undefined literal on line: ' +
                        str(self._line_number+1), code=1,
                        contents=self._contents)
            
            
        disp = twos_complement(int(self._disp, 16), 20)

        # flags
        flags = to_binary(hex(self._flags)) 

        # combine each section
        output += op
        output += flags.zfill(4)
        output += disp

        hex_output = hex(int(output, 2))[2:].zfill(8).upper()

        return  hex_output
         


    def __len__(self):
        return 4

    def __repr__(self):
        return "<Format4: mnemonic=%s n=%s i=%s flags=%s disp=%s>" % \
                (self._mnemonic, self._n, self._i, self._flags, self._disp)
    







