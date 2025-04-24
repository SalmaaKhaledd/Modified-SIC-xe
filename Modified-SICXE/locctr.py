from srcLine import *
from block import *
from formats import *
from instruction import *
from errors import *


class Location_Ctr():
     
     def __init__(self):
          self.locctrs=[0,0,0,0]  
          #0-> DEFAULT 
          #1-> DEFAULTB
          #2-> CDATA
          #3-> CBLKS
          
     
     def updateLocctr(self, source_line):
          mnemonic=source_line.mnemonic
          operand = source_line.operand
          block_no=source_line.block_no

          print("locctr...")
          

          # if block_no is not None:
         
          if (mnemonic == 'WORD'):
                self.locctrs[block_no] += 3
                print(self.locctrs[block_no])
          elif (mnemonic == 'RESW'):
                    self.locctrs[block_no] += 3 * int(operand)
          elif mnemonic == 'RESB':
                    self.locctrs[block_no] += int(operand)
          elif mnemonic == 'BYTE':
                  print(operand)
                  if hex_value(operand):  
                    operand= operand[2:-1]  #operand in hex without X''
                    self.locctrs[block_no]+= int(len(operand)/ 2)
                    print(self.locctrs[block_no])
                  elif ascii_value(operand):
                    operand= operand[2:-1]  #operand in hex without C''
                    self.locctrs[block_no]+= len(operand)
                  else:
                        raise LineFieldsError( message="Invalid value for BYTE on line: " )
                              
          elif(base_mnemonic(mnemonic) in op_table):
              format=determine_format(mnemonic)
              if(format==1):
                  print("format 1")
                  self.locctrs[block_no]+=1
              elif(format==2):
                  print("format 2")
                  self.locctrs[block_no]+=2
              elif(format==3):
                  print("format 3")
                  self.locctrs[block_no]+=3
              elif(format==4):
                  print("format 4")
                  self.locctrs[block_no]+=4
          else :
                  print(source_line.mnemonic)
                  raise InvalidOpcodeError(  message='The mnemonic is invalid on line: ')
          print(self.locctrs)
                  
       
                
     def handle_LTORG(self, littab):
           print("handle ltorg")
           print(littab)
           for key,value in littab.items():
              address=value[2]
              if(address is None):
                 address=self.locctrs[2]
                 value[2]=address
                 self.locctrs[2]+=value[1]  #value[1] is the length of the literal
                 print("lit length")
                 print(value[1])
                 print("address")
                 print(address)
           
           print(self.locctrs)
           print(littab)
           return littab
     
def base_mnemonic(mnemonic):
        print("base mnemonic")
        if extended(mnemonic):
           print(mnemonic[1:])
           return mnemonic[1:]
        else:
           print(mnemonic)
           return mnemonic
   
  
   
  
             
              
           
           

           
           
           
           
           
           

            
               
               

               
          


          
     