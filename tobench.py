# -------------------------------------------------------------------------------
# Copyright 2021, Benjamin Tan <benjamin.tan@nyu.edu>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -------------------------------------------------------------------------------


import sys
import argparse
import re

def main():

    INFO = "Post-Synthesis Verilog Netlist to Bench"
    VERSION = 0.1
    USAGE = "Usage: python3 tobench.py -i INPUT_FILE -o OUTPUT_FILE"

    def showVersion():
        print(INFO)
        print(VERSION)
        print(USAGE)
        sys.exit()

    argparser = argparse.ArgumentParser(description="Assumes only one verilog module in file")
    argparser.add_argument("-V", "--version", action="store_true", dest="showversion", default=False, help="Show the version")
    argparser.add_argument("-i", "--input_file", action="store", dest="input_file", default="", help="Specify the name of the netlist file to process")
    argparser.add_argument("-o", "--output_file", action="store", dest="output_file", default="out.bench", help="Specify the name of the output file")
    argparser.add_argument("--for_formal_check_reg", action="store_true", dest="formality_aid", default=False, help="Try to keep reg names")

    # read arguments/options from the cmd line
    args = argparser.parse_args()

    if args.showversion:
        showVersion()
    
    if args.input_file == '':
        args.input_file = args[0]
    
    print("Reading File: " + args.input_file)

    with open(args.input_file, 'r') as f:
        line = ''
        with open(args.output_file, 'w') as outfile:

            while True:
                line += f.readline()
                if "endmodule" in line: # assume that netlist file has only one module!
                    break
                elif "//" == line[:2]: # ignore lines that start with comments ... e.g., synopsys header
                    line = ''
                elif ";" in line: # once we've reached the end of a statement
                    line = ' '.join(line.split()) # get rid of multiple spaces and trailing spaces
                    line = line.replace('\n','') # get rid of newlines in the middle of an instantiation
                    outfile.write(process_cell(line, args.formality_aid))
                    line = ''
            
        print("done")

def process_cell(line, formal_help):
    newline = ''

    if "input " in line:
        to_process = line.replace("input ","").replace(' ', '').replace(";",'').split(",")
        # print(to_process)
        for port in to_process:
            newline += "INPUT(" + port + ")\n"
        return newline
    elif "output " in line:
        to_process = line.replace("output ","").replace(' ', '').replace(";",'').split(",")
        # print(to_process)
        for port in to_process:
            newline += "OUTPUT(" + port + ")\n"
        return newline
    elif "module " in line:
        return "###\n"
    elif "wire " in line:
        return ""

    # newline = line.replace(' ','')
    # to_process = newline.split(",")

    ### Continue on for regular nodes

    # extract node type and name
    test = line.split(" ")
    test = test[:2]

    newline = line.replace(' ','')
    to_process = newline.split(",")
    
    if "INV" in test[0]:
        newline = (re.search( ".ZN\((.*?)\)", str(to_process)).group(1) + " = NOT(" + re.search( ".I\((.*?)\)", str(to_process)).group(1) + ")")
    elif "BUF" in test[0]:
        newline = (re.search( ".Z\((.*?)\)", str(to_process)).group(1) + " = BUF(" + re.search( ".I\((.*?)\)", str(to_process)).group(1) + ")")
    elif "NAND" in test[0]:
        newline = (re.search( ".ZN\((.*?)\)", str(to_process)).group(1) + " = NAND(" + re.search( ".A1\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".A2\((.*?)\)", str(to_process)).group(1) +")")
    elif "AND" in test[0]:
        newline = (re.search( ".Z\((.*?)\)", str(to_process)).group(1) + " = AND(" + re.search( ".A1\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".A2\((.*?)\)", str(to_process)).group(1) +")")
    elif "XNOR" in test[0]:
        newline = (re.search( ".ZN\((.*?)\)", str(to_process)).group(1) + " = XNOR(" + re.search( ".A1\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".A2\((.*?)\)", str(to_process)).group(1) +")")
    elif "XOR" in test[0]:
        newline = (re.search( ".Z\((.*?)\)", str(to_process)).group(1) + " = XOR(" + re.search( ".A1\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".A2\((.*?)\)", str(to_process)).group(1) +")")
    elif "NOR" in test[0]:
        newline = (re.search( ".ZN\((.*?)\)", str(to_process)).group(1) + " = NOR(" + re.search( ".A1\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".A2\((.*?)\)", str(to_process)).group(1) +")")
    elif "OR" in test[0]:
        newline = (re.search( ".Z\((.*?)\)", str(to_process)).group(1) + " = OR(" + re.search( ".A1\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".A2\((.*?)\)", str(to_process)).group(1) +")")
    elif "DFF" in test[0]:
        if formal_help:
            newline = test[1] + " = DFF(" + re.search( ".D\((.*?)\)", str(to_process)).group(1)+ ")\n"
            newline += re.search( ".Q\((.*?)\)", str(to_process)).group(1) + " = BUF(" + test[1] + ")"
        else:
            newline = (re.search( ".Q\((.*?)\)", str(to_process)).group(1) + " = DFF(" + re.search( ".D\((.*?)\)", str(to_process)).group(1)+ ")")

    else:
        newline = line
    return newline + '\n'

if __name__ == "__main__":
    main()