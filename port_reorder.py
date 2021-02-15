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

    INFO = "Port Reorder-er"
    VERSION = 0.1
    USAGE = "Usage: python3 port_reorder.py -i INPUT_FILE -o OUTPUT_FILE"

    def showVersion():
        print(INFO)
        print(VERSION)
        print(USAGE)
        sys.exit()

    argparser = argparse.ArgumentParser(description="Assumes only one verilog module in file")
    argparser.add_argument("-V", "--version", action="store_true", dest="showversion", default=False, help="Show the version")
    argparser.add_argument("-i", "--input_file", action="store", dest="input_file", default="", help="Specify the name of the netlist file to process")
    argparser.add_argument("-o", "--output_file", action="store", dest="output_file", default="reorder.bench", help="Specify the name of the output file")

    # read arguments/options from the cmd line
    args = argparser.parse_args()

    if args.showversion:
        showVersion()
    
    if args.input_file == '':
        args.input_file = args[0]
    
    print("Reading File: " + args.input_file)
    primaryInputs = []
    primaryOutputs = []
    keyinputs = []

    with open(args.input_file, 'r') as f:
        line = ''
        while True:
            line += f.readline()
            # print(line)
            if len(line) == 0 : # reached the end!
                break
            elif "#" in line:
                pass
            elif "INPUT" in line:
                if "keyinput" in line:
                    keyinputs.append(line)
                else:
                    primaryInputs.append(line)
            elif "OUTPUT" in line: 
                primaryOutputs.append(line)
            else:
                break
            line = ''
    
    primaryInputs.sort(reverse=True)
    primaryOutputs.sort(reverse=True)
    keyinputs.sort(reverse=True)

    # sort the ports as desired
    primaryInputs.sort(reverse=True,key=len)
    primaryOutputs.sort(reverse=True,key=len)
    keyinputs.sort(reverse=True,key=len)

    with open(args.output_file, 'w') as o:
        for port in primaryInputs:
            o.write(port)
        for port in primaryOutputs:
            o.write(port)
        for port in keyinputs:
            o.write(port)
        with open(args.input_file, 'r') as f:
            line = ''
            while True:
                line += f.readline()
                # print(line)
                if len(line) == 0 : # reached the end!
                    break
                elif "#" in line:
                    pass
                elif "INPUT" in line:
                    pass
                elif "OUTPUT" in line: 
                    pass
                else:
                    o.write(line)
                line = ''

    print("done")

if __name__ == "__main__":
    main()