from tables import block_table
from errors import *
class Block(object):
     def __init__(self):
          
          self.block_table=block_table
          self.currBlock=0
          self.finalBlcks=dict() #final block table
     def switchBlock(self, blockName):
          block_no=block_table[blockName]
          if(block_no==self.currBlock):
               return self.currBlock
          else: 
               self.currBlock=block_no
               return self.currBlock
          
     def assign_address(self,locctr):
         for blockName, block_no in block_table.items():
             if blockName not in block_table:
                  raise UndefinedBlockError("This block does not exist")
             
             if block_no==0: 
                  addr=0
                  self.finalBlcks[block_no] = {"name": blockName,"length":locctr[block_no]  ,"address":addr }
             else: 
                  prev_block=int(block_no)-1
                  addr=self.finalBlcks[prev_block]["address"]+self.finalBlcks[prev_block]["length"]
                  self.finalBlcks[block_no] = {"name": blockName,"length":locctr[block_no]  ,"address":addr }


     def turn_into_text(self):  #for testing purposes only
         for block_no, block_data in self.finalBlcks.items():
             print(f"{block_no} : {block_data['name']}, {block_data['length']}, {block_data['address']}\n")

     def sum_of_addresses(self):
        total_address = sum(block_data["length"] for block_data in self.finalBlcks.values()) 
        return total_address
   
               
          
          


      

    