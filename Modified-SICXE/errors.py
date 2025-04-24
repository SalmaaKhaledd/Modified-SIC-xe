
class BaseError(Exception):
    def __init__(self, message):
        self.message = message
        

    def __str__(self):
        return (self.message)

#pass1 errors

class DuplicateSymbolError(BaseError): #raise in symbol table
    def __init__(self):
        super(DuplicateSymbolError, self).__init__()

   
class InvalidOpcodeError(BaseError): 
    def __init__(self):
        super(InvalidOpcodeError, self).__init__()

class LineFieldsError(BaseError): 
    def __init__(self):
        super(LineFieldsError, self).__init__()

#pass2 errors

class UndefinedSymbolError(BaseError):  
    def __init__(self):
        super(UndefinedSymbolError, self).__init__()

class InstructionError(BaseError): 
    def __init__(self):
        super(InstructionError, self).__init__()

class UndefinedBlockError(BaseError):
    def __init__(self):
        super(UndefinedBlockError, self).__init__()


