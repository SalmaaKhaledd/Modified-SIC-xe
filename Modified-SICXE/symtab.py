from errors import DuplicateSymbolError, UndefinedSymbolError

class symbol_table:

    def __init__(self):
        self.symtab = dict() 
        """key --> string --> label
           value --> tuple --> (location, blockno)
        """

    def insert_label(self, label, loc_ctr, blk_no):
        if label is not None:
            if label not in self.symtab:
                self.symtab[label] = (hex(int(loc_ctr))[2:].zfill(4), int(blk_no))       
            else:
                raise DuplicateSymbolError(f"Symbol {label} already exists")
      
    def retrieve_label(self, label):
        if label in self.symtab:
            location, blockno = self.symtab[label]
            return location, blockno
        else: 
            raise UndefinedSymbolError(f"Symbol {label} does not exist")
        
    def modify_addresses(self, finalBlcks):
        updated_symtab = {}
        for label, (location ,blockno) in self.symtab.items():
            blkno = int(blockno)
            loc = int(location, 16)
            abs_location = loc + int(finalBlcks[blkno]["address"] )
            abs_location = hex(abs_location)[2:].zfill(4).upper()
            updated_symtab[label] = [abs_location, blockno]
        self.symtab = updated_symtab

    def turn_into_text(self, outputfile):
        with open(outputfile, 'w') as file:
            file.write(f"{'Label':<20}{'Location':<20}{'Block No':<10}\n")
            file.write("="*50 + "\n")
            for label, (location, blockno) in self.symtab.items():
                location = location.upper()
                file.write(f"{label:<20}{location:<20}{blockno:<10}\n")
    
