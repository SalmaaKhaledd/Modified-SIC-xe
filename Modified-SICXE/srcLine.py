from errors import LineFieldsError

class srcLine(object):
  def __init__(self, lineNum, label, mnemonic, operand,loc,block_no):
        self.lineNum = lineNum
        self.label = label
        self.mnemonic = mnemonic
        self.operand = operand
        self.loc = loc
        self.block_no= block_no
        self.objCode=None
        self.instruction_flag=None
 

  @staticmethod
  def parse(line, lineNum):
        """ Parse an individual line and return a SourceLine object. """
    
        fields=line.split()  #split on whitespaces
        
       #ex: label CADD S, LABEL2, V

        if len(fields) > 3 and fields[1].endswith(',') and fields[2].endswith(','): #without label
            operands = fields.pop(1) + fields.pop(1) + fields.pop(1)
            fields.append(operands) #operand = S,LABEL2,V
        elif len(fields) > 3 and fields[2].endswith(',') and fields[3].endswith(','): #with label
            operands = fields.pop(2) + fields.pop(2) + fields.pop(2)
            fields.append(operands) 
        elif len(fields) > 1 and fields[1].endswith(','):
            operands = fields.pop(1) + fields.pop(1)
            fields.append(operands)
        elif len(fields) > 2 and fields[2].endswith(','):
            operands = fields.pop(2) + fields.pop(2)
            fields.append(operands)
          
        
        if len(fields) == 3:
            return srcLine(label=fields[0], mnemonic=fields[1],
                              operand=fields[2], lineNum=lineNum,loc=None, block_no=None)
        elif len(fields) == 2:
            return srcLine(label=None, mnemonic=fields[0],
                              operand=fields[1], lineNum=lineNum,loc=None, block_no=None)
        elif len(fields) == 1:
            return srcLine(label=None, mnemonic=fields[0], operand=None,
                              lineNum=lineNum,loc=None, block_no=None)
        else:
            
            raise LineFieldsError(message='Invalid amount of fields on line:')
                    
                   
        
  def __repr__(self):
        return "<SourceLine: %s, %s, %s, %s, %s, %s,%s,%s>" % (self.lineNum, self.label, self.mnemonic,
                                             self.operand,self.loc, self.block_no, self.objCode, self.instruction_flag)


        

 