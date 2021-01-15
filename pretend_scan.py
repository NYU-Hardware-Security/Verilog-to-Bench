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
import fileinput


def main():

    INFO = "Sequential --> Combinational (Emulates Scan Access)"
    VERSION = 0.1
    USAGE = "Usage: python3 pretend_scan.py -i INPUT_FILE -o OUTPUT_FILE"

    def showVersion():
        print(INFO)
        print(VERSION)
        print(USAGE)
        sys.exit()

    argparser = argparse.ArgumentParser(description="Assumes only one verilog module in file")
    argparser.add_argument("-V", "--version", action="store_true", dest="showversion", default=False, help="Show the version")
    argparser.add_argument("-i", "--input_file", action="store", dest="input_file", default="", help="Specify the name of the netlist file to process")
    argparser.add_argument("-o", "--output_file", action="store", dest="output_file", default="scanned.bench", help="Specify the name of the output file")

    # read arguments/options from the cmd line
    args = argparser.parse_args()

    if args.showversion:
        showVersion()
    
    if args.input_file == '':
        args.input_file = args[0]
    
    print("Reading File: " + args.input_file)

    with open(args.input_file, 'r') as f:
        line = ''
        with open("tempfile", 'w') as tempin: # file for the inputs of the bench
            with open("tempfile2", 'w') as tempout: # file for outputs of the bench
                with open("tempfile3", 'w') as outfile: # file for all the internal nodes
                    while True:
                        line += f.readline()
                        # print(line)
                        if len(line) == 0 : # reached the end!
                            break
                        elif "#" in line:
                            pass
                        elif "INPUT" in line:
                            tempin.write(line)
                        elif "OUTPUT" in line: 
                            tempout.write(line)
                        elif "DFF" in line: # this is the crucial part, inputs to DFFs become POs, outputs to DFFs become PIs
                            # print(line.split(" "))
                            line = line.replace(" ","")
                            flip_in = re.search("DFF\((.*?)\)", str(line)).group(1)
                            flip_out = re.search("(.*?)=", str(line)).group(1)
                            tempin.write("INPUT(newin_" + flip_out + ")\n")
                            outfile.write(flip_out + " = BUF(newin_" + flip_out + ")\n")
                            tempout.write("OUTPUT(newout_" + flip_in + ")\n")
                            outfile.write("newout_" + flip_in + " = BUF(" + flip_in + ")\n")
                        else:
                            outfile.write(line)
                        line = ''

    # finish off by combining the files        
    with fileinput.input(files=('tempfile', 'tempfile2', 'tempfile3')) as f:
        with open(args.output_file, 'w') as o:
            for line in f:
                o.write(line)
    
    
    print("done")

if __name__ == "__main__":
    main()