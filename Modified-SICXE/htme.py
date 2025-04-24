from formats import *

def generate_records(generated_objects, program_name, start_address, program_length):
    print("started records")
   #create an empty list to store htme records
    htme = []

    header_rec = gen_header(program_name, start_address, program_length)
    htme.append(header_rec)  #adds header_rec to htme
    print("h appended")
    texts = gen_text(generated_objects)
    for record in texts:
        htme.append(record)
    print("t appended")

    mods = gen_mod(generated_objects)
    for record in mods:
        htme.append(record)
    print("m appended")
    end_rec = gen_end(start_address)
    htme.append(end_rec)   #adds end_rec to htme
    print("e appended")
    return htme


def gen_header(program_name, start_address, program_length):
    print("h records")
    title = "H"
    prog_name = str(program_name).ljust(6, "x").upper()                      
    start_add = hex(start_address)[2:].zfill(6).upper()
    prog_length = hex(int(program_length))[2:].zfill(6).upper()
    print(title + prog_name + start_add + prog_length)
    return title + prog_name + start_add + prog_length

def gen_end(starting_address):
    print("e records")
    title = "E"
    prog_start = hex(starting_address)[2:].zfill(6).upper() 
    print(title + prog_start)
    return title + prog_start


def gen_text(generated_objs):
     print("t records")
     objectcodes = list(generated_objs) #each generated object is a tuple --> (object code, inst_flag,line_num, location )
     max_bytes = 60 
     all_Text_Records = []

     #temp vars to store values of each T record
     temp_line = []  
     temp_startadd = 0
     temp_length = 0

     while(len(objectcodes) > 0):  #loops on each object code line
        object_codes_column = ""
        
        while((len(object_codes_column) + len(str(objectcodes[0][0]))) <= max_bytes): #generate 1 T record
            x = objectcodes.pop(0)
            inst_flag = x[1] 
            
            if inst_flag is None:
                break 

            else:
                temp_contents = x[0]
            
            object_codes_column = object_codes_column + temp_contents
            temp_length += len(temp_contents)/2  #2 hex digits/byte 
            if temp_startadd == 0:
                temp_startadd = x[3]
            
            if len(objectcodes) is 0:
                break

        temp_startadd = hex(int(temp_startadd))[2:].zfill(6).upper()
        temp_length = hex(int(temp_length))[2:].zfill(2).upper()
        temp_line = "T%s%s%s" % (temp_startadd, temp_length, object_codes_column)
        print(f"temp_length {temp_length}") #formats the list into string
        if(int(temp_length,16) != 0):
            all_Text_Records.append(temp_line)
        
        temp_line = []
        temp_startadd = 0
        temp_length = 0
     print(all_Text_Records)
     return all_Text_Records  


def gen_mod(generated_objs):
     objectcodes = list(generated_objs) #each generated object is a tuple --> (location, object code)
     all_Mod_Records = [] #list of all M records
     #temp vars to store values of each M record
     temp_line = [] 
     temp_add = 0

     first_element = objectcodes[0][0]
     print(f"First element: {first_element}")
     print(f"Length of first element: {len(str(first_element))}")
     
     while(len(objectcodes) > 0):  #loops on each object code line
        print("entered loop")
        if objectcodes[0][0] is None:
            print("NoneType found, removing element")
            objectcodes.pop(0)  # Remove the element if it is None
            continue
        if(len(str(objectcodes[0][0])) == 8):
           x = objectcodes.pop(0)
           temp_add = str(x[3]) 
           temp_add = hex(int(x[3])+1)[2:].zfill(6).upper()
           temp_line = "M%s05" % (temp_add)
           all_Mod_Records.append(temp_line)
       
        else:
            objectcodes.pop(0)
            continue
     print(all_Mod_Records)
     return all_Mod_Records




           
        