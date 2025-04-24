import re

def blank_line(line):
    return len(line.strip()) == 0


def remove_comments(line):
    if ';' in line:  # Check if there's a comment character
        return line.split(';')[0].rstrip()  # Keep everything before the comment
    return line.rstrip()  # Return the original line if no comment


def remove_line_number(line):
    # Use regex to remove leading line numbers (digits followed by spaces)
    return re.sub(r'^\d{1,}\s{3}', '', line) # Match digits followed by spaces at the start

def process_input_file(inputFile, interFile):
     try:
          with open(inputFile, 'r') as inputFile, open(interFile, "w") as interFile:
               for line in inputFile:  # Read each line as a string
                   if not blank_line(line):  # Ignore blank lines
                    cleaned_line = remove_comments(line)
                    cleaned_line = remove_line_number(cleaned_line)  # Remove comments
                    interFile.write(cleaned_line + "\n")  
               
     except FileNotFoundError:  
        print(f"Error: {inputFile} not found.")

def proces_outPass2(interFile, outfile, updated_contents):
    try:
        with open(interFile, 'r') as interFile, open(outfile, "w") as outfile:
            count = 0
            lines = interFile.readlines()  # Read all lines into memory
            while count < 35:  # Loop through the 35 elements in updated_contents
                line = lines[count]  # Get the line corresponding to the current count
                if not blank_line(line): 
                    if count == 0:
                        outfile.write(line)
                    else:
                        if updated_contents[count-1].objCode is None:
                            new_line = line.rstrip() + "      " + "\n"
    
                        else:
                            new_line = line.rstrip() + "      " + str(updated_contents[count-1].objCode) + "\n"
                        outfile.write(new_line)
                    count += 1
            outfile.write(lines[35])  
            outfile.write(lines[36]) 
    except FileNotFoundError:
        print(f"Error: {interFile} not found.")

def process_outPass1(interFile, outfile, temp_contents):
     try:
        with open(interFile, 'r') as interFile, open(outfile, "w") as outfile:
            count = 0
            lines = interFile.readlines()  # Read all lines into memory
            while count < 35:  # Loop through the 35 elements in updated_contents
                line = lines[count]  # Get the line corresponding to the current count
                if not blank_line(line): 
                    if count == 0:
                        outfile.write(line)
                    else:
                        if temp_contents[count-1].loc is None:
                            new_line = line.rstrip() + "         " + "\n"
                        elif temp_contents[count-1].mnemonic == "USE" or temp_contents[count-1].mnemonic == "BASE":
                            new_line = line.rstrip() + "      " + "\n"
                        else:
                            
                            new_line = line.rstrip() + "          " + hex(temp_contents[count-1].loc)[2:].upper()+ "\n"
                        outfile.write(new_line)
                    count += 1
            outfile.write(lines[35])  
            outfile.write(lines[36]) 
     except FileNotFoundError:
        print(f"Error: {interFile} not found.")
    
                  
   