from instruction import *


class Literal:
      def __init__(self):
          self.littab=dict()
          
    
      def insert_littab(self,operand):
          print("literals...")
          if operand not in self.littab:
              if hex_value(operand):
                  value=operand[2:-1]
                  length=len(value)/2
                  address=None
                  self.littab[operand]=[value,length,address]

              elif ascii_value(operand):
                   operand_new=operand[2:-1]
                   value =''.join(hex(ord(char))[2:] for char in operand_new) #ascii value
                   length=len(operand_new)
                   address=None
                   self.littab[operand]=[value,length,address]

      def adjust_address(self,finalBlcks,symtab):  #adjust addresses of literals to rel block & add to symbol table
            updated_littab = {}
            for name, (value,length,address) in self.littab.items():
                    new_address = address + finalBlcks[2]["address"] 
                    updated_littab[name] = [value, length, new_address]
                    symtab.insert_label(name,new_address,2)
            self.littab = updated_littab
            print("adjusted address")
            print(self.littab)

   
                     
        

      def turn_into_text(self):  #for testing purposes only
         for name, (value,length,address) in self.littab.items():
            print(f"{name} : {value} , {length} , {address}\n")

         
            
      def retrieve_lit(self,literal):
          if literal in self.littab:
              value,length,address=self.littab[literal]
              return [value,length,address]
          else:
              raise ValueError(f"Literal {literal} does not exist")
         
                  

      def extractLitValue(literal):
         if hex_value(literal):  
            return literal[2:-1] 
         elif ascii_value(literal):
            return literal[2:-1]
         elif literal == "*":  # Current location counter literal
            return literal, '*'  # Placeholder value, LC will be assigned later
         else:
            raise ValueError(f"Unsupported literal format: {literal}")