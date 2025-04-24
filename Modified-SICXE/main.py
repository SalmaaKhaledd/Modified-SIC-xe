import argparse
import re
from literals import *
from srcLine import *
from instruction import *
from tables import op_table
from assembler import *
from locctr import *
from files_processing import *





def blank_line(line):
    return len(line.strip()) == 0


def remove_comments(line):
    if ';' in line:  # Check if there's a comment character
        return line.split(';')[0].rstrip()  # Keep everything before the comment
    return line.rstrip()  # Return the original line if no comment


def remove_line_number(line):
    # Use regex to remove leading line numbers (digits followed by spaces)
    return re.sub(r'^\d{1,}\s{3}', '', line) # Match digits followed by spaces at the start

def process_file(inputFile, interFile, outFile):
     try:
          with open(inputFile, 'r') as inputFile, open(interFile, "w") as interFile:
               for line in inputFile:  # Read each line as a string
                   if not blank_line(line):  # Ignore blank lines
                    cleaned_line = remove_comments(line)
                    cleaned_line = remove_line_number(cleaned_line)  # Remove comments
                    interFile.write(cleaned_line + "\n")  
               
     except FileNotFoundError:  
        print(f"Error: {inputFile} not found.")
   
              


def main():
    try:
            with open('intermediate.txt', 'r') as f:
                a = Assembler(f)
                a.assemble()
    except IOError:
            print("[IO Error]: The source file could not be opened.")
    except InvalidOpcodeError as e:
            print("[OpcodeLookupError] information:")
            print(e.details)
            raise
            

   

if  __name__ == "__main__":
    parser = argparse.ArgumentParser(description='SIC/XE Assembler')
    parser.add_argument('--input', required=True, help='Input assembly file')
    parser.add_argument('--output', default='output.txt', help='Path for the output object file (optional)')
    args = parser.parse_args()
    process_input_file(args.input,'intermediate.txt')
    main()
     
    