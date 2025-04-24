from srcLine import *
from block import *
from symtab import *
from locctr import *
from tables import *
from literals import *
from formats import *
from format1 import *
from format2 import *
from format4 import *
from format4f import *
from format3 import *
from instruction import *
import codecs
from htme import *
from files_processing import *


class Assembler(object):

   def __init__(self, interFile):
        
        self.contents = (line.rstrip('\n') for line in interFile.readlines())
        # Location counter
        self.locctrs=Location_Ctr() #list -> access using block num as index
        self.block=Block()
        self.currBlock = 0  #by defualt --> DEFAULT block
        #program starting address
        self.start_address = 0
        # Symbol table
        self.symtab = symbol_table() #initialize symbol class --> creates symtab
        #literal table
        self.litObj= Literal()
        # Program length
        # BASE register
        self.base = None
        self.program_length = 0
        # Program name
        self.program_name = ""
        # Temporary array to store results of the first pass
        self.temp_contents = []
        # array of tuples containing debugging information
        self.__generated_objects = []
        # array of the generated records
        self.__generated_records = []
        self.object_List=[]


   
                    
      

  #add constructor
   def assemble(self):
      #if len(self.__generated_records) == 0:
               self.pass1()
               self.pass2()
               self.__generated_records = generate_records(self.object_List,self.program_name,self.start_address,self.program_length)
               with open('HTME.txt', 'w') as file:
                    for item in  self.__generated_records:
                         file.write(f"{item}\n")

      #return self.generated_records --> print to txt instead
     
   def pass1(self):
        
        first = next(self.contents) #first line
        first_line = srcLine.parse(first, lineNum=1) #parse first line
       

        if first_line.mnemonic is not None:  #handle else
             if first_line.mnemonic == 'START':
                   self.program_name = first_line.label
                   self.start_address = 0 
                   print("prog name")
                   print(self.program_name)
                   print("starting prog address")
                   print(self.start_address)
         
         # Loop through every line excluding the first
        for line_number, line in enumerate(self.contents):
             source_line = srcLine.parse(line, line_number+2)
             source_line.block_no=self.currBlock
             print("source line .....")
             print(source_line)
             print("block no:")
             print(source_line.block_no)
             source_line.loc= self.locctrs.locctrs[source_line.block_no]
             print("loc counter:")
             print(source_line.loc)

             if source_line.mnemonic=="USE":
                  if source_line.operand is None:
                       source_line.operand="DEFAULT"
                       self.currBlock=self.block.switchBlock(source_line.operand)
                  else:
                       self.currBlock=self.block.switchBlock(source_line.operand)
                  print("new block")
                  print(self.currBlock)
                  

             elif source_line.mnemonic == 'LTORG':
                  self.litObj.littab=self.locctrs.handle_LTORG(self.litObj.littab)
             elif source_line.mnemonic == 'BASE':
                    pass
             elif source_line.mnemonic == 'END':
                  break
             else :
                    self.locctrs.updateLocctr(source_line)
                    if literal(source_line.operand):
                       self.litObj.insert_littab(source_line.operand[1:])
                       self.litObj.turn_into_text()
                    else:
                       print("going in symtab")
                       self.symtab.insert_label(source_line.label, source_line.loc, source_line.block_no)
             # Add to the temporary array
             
             self.temp_contents.append(source_line)  #list of all source lines

        self.block.assign_address(self.locctrs.locctrs)
        self.symtab.turn_into_text("symbols.txt")
        print(self.temp_contents)
        print("block addresses")
        self.block.turn_into_text()
        process_outPass1("intermediate.txt","out_pass1.txt",self.temp_contents) 
        

   def pass2(self):
         self.symtab.modify_addresses(finalBlcks=self.block.finalBlcks) #function to update symbol table
         self.litObj.adjust_address(finalBlcks=self.block.finalBlcks,symtab=self.symtab) #function to update literal table
         self.symtab.turn_into_text("symbols2.txt")
         self.litObj.turn_into_text() #for testing purposes only
         self.program_length = self.block.sum_of_addresses()
         
         updated_contents=[]
         for source_line in self.temp_contents:
              block_no=source_line.block_no
              block_address=self.block.finalBlcks[block_no]["address"]
              source_line.loc+=block_address  #update location counter for all srcLines
              updated_contents.append(source_line)
         print("updated contents")
         print(updated_contents) #list of all source lines after updating due to pass 2

              

         object_code = []
         for source_line in updated_contents:
          found_opcode = op_table.get(base_mnemonic(source_line.mnemonic))
          print(source_line.mnemonic)
          
          if found_opcode:
               instr_format = determine_format(source_line.mnemonic)
               objCode = self.generate_instruction( source_line.lineNum,instr_format, source_line) 
               object_code.append((source_line.loc, objCode,source_line)) #adds tuple to objCode list

          else: #extract object_info -->location & hex value of operand
               if source_line.mnemonic == 'WORD':  
                    hexValue = hex(int(source_line.operand))
                    stripped_value = hexValue.lstrip("0x")
                    padded_value = stripped_value.zfill(6) 
                    object_info = (source_line.mnemonic, source_line.operand,padded_value)
                    object_code.append((source_line.loc, object_info,source_line))
               elif source_line.mnemonic == 'BYTE':
                    if hex_value(source_line.operand):
                        value = source_line.operand.replace("X", '')
                        stripped_value = value.replace("'", '') #removes quotes --> value remains in hexa
                        object_info = (source_line.mnemonic, source_line.operand, stripped_value)
                        object_code.append((source_line.loc, object_info,source_line))
               elif ascii_value(source_line.operand):
                        value = source_line.operand.replace("C", '')
                        stripped_value = value.replace("'", '').encode() #converts string to its byte representation
                        hexValue = codecs.encode(stripped_value, "hex")  #Converts the byte representation of the string into a hexadecimal string.
                        object_info = (source_line.mnemonic,source_line.operand, hexValue)
                        object_code.append((source_line.loc, object_info,source_line))
               elif source_line.mnemonic == 'BASE':
                    self.base,blk_no = self.symtab.retrieve_label(source_line.operand)
               elif source_line.mnemonic == 'LTORG':
                    
                    print("-----------lit----------")
                    print("-----------lit----------")
                    print("-----------lit----------")
                    print("-----------lit----------")
                    print("-----------lit----------")
                    Literal_list = list(self.litObj.littab.values())
                    print(Literal_list)                  
                    Lit_info = Literal_list.pop(0)
                    print("lit info")
                    print(Lit_info)
                    object_code.append((None, Lit_info, source_line))
                    
               elif source_line.mnemonic == 'USE' or 'RESB'  or 'RESW':
               
                    object_code.append((source_line.loc, None ,source_line))
                    

         self.__generated_objects = object_code
         print("object code")
         print(object_code)   
     

         list_copy=list(object_code)
         self.object_List=self.generate_objectList(list_copy) #used in records generation (objCode,flag,lineNum,loc)
         #updated_contents list now contains source lines with object code & all updated data (flag and updated locctr)
         print("updated contents")
         print(updated_contents)
         proces_outPass2("intermediate.txt","out_pass2.txt",updated_contents) 
   
              

   def generate_objectList(self,list_copy):
          objectList=[]
          for i in range(len(list_copy)):
               instruct_flag=False
               x = list_copy.pop(0)
               if isinstance(x[1], Format): 
                    instruct_flag=True
                    objCode = x[1].generate()
                    x[2].objCode=objCode #update source line with object code
                    x[2].instruction_flag=instruct_flag #update source line with flag
                    objectList.append((objCode,instruct_flag,x[2].lineNum,x[0]))
               elif x[1] is None:
                    instruct_flag = None
                    objectList.append((None,instruct_flag, x[2].lineNum, x[0]))
               elif x[0] is None:
                    objCode = x[1][0]
                    objectList.append((objCode, instruct_flag, x[2].lineNum, x[1][2] ))
               else:
                    objCode = x[1][2]
                    x[2].objCode=objCode #update source line with object code
                    x[2].instruction_flag=instruct_flag #update source line with flag
                    objectList.append((objCode, instruct_flag, x[2].lineNum, x[0]))
          print("object list")
          print(objectList)
          return objectList
           


   def generate_instruction(self, line_number, instr_format, source_line):
        if instr_format == 1:
            instruction = Format1(mnemonic=source_line.mnemonic)

        elif instr_format == 2:
            expected_operands = op_table[source_line.mnemonic].operands
            if len(expected_operands) == 2:
                r1, r2 = source_line.operand.split(',')
            elif len(expected_operands) == 1:
                r1, r2 = source_line.operand, None
            instruction = Format2(mnemonic=source_line.mnemonic, r1=r1, r2=r2)


        elif instr_format == 3:
            print("format 3")
            instruction = Format3(base=self.base, symtab=self.symtab,littab=self.litObj,source_line=source_line)

                                  
        elif instr_format == 4  and extended(source_line.mnemonic):
          
            instruction = Format4(symtab=self.symtab,littab=self.litObj, source_line=source_line)


        elif instr_format == 4:
               expected_operands = op_table[source_line.mnemonic].operands
               if len(expected_operands) == 3:
                    r, label, f = source_line.operand.split(',')
                    address, blk = self.symtab.retrieve_label(label)
               elif len(expected_operands) == 2:
                    r = None
                    label, f = source_line.operand.split(',')
                    address, blk = self.symtab.retrieve_label(label)
               instruction = Format4f(mnemonic = source_line.mnemonic, r= r, f= f, address = address)

        return instruction
                    
                                                   


def base_mnemonic(mnemonic):
        print("base mnemonic")

        if extended(mnemonic):
           print(mnemonic[1:])
           return mnemonic[1:]
        else:
           print(mnemonic)
           return mnemonic
   
  
 

             




             






                  

        

        



  